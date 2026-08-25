import { after, describe, test } from "node:test";
import assert from "node:assert/strict";
import { execSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const productionLoader = path.join(repoRoot, ".opencode", "plugins", "majestic-abilities.js");
const fixtures = [];

function makeRoot(prefix) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), prefix));
  fixtures.push(dir);
  return fs.realpathSync(dir);
}

function writeSkill(skillDir, body) {
  fs.mkdirSync(skillDir, { recursive: true });
  fs.writeFileSync(path.join(skillDir, "SKILL.md"), body);
}

function skillDoc(name, description) {
  return ["---", "name: " + name, "description: " + description, "---", "", "# " + name, ""].join(
    "\n",
  );
}

function writeLoader(fixtureRoot) {
  const dest = path.join(fixtureRoot, ".opencode", "plugins", "majestic-abilities.js");
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(productionLoader, dest);
  return dest;
}

function copyCoreSkills(fixtureRoot) {
  const dest = path.join(fixtureRoot, "plugins", "core", "skills");
  fs.cpSync(path.join(repoRoot, "plugins", "core", "skills"), dest, { recursive: true });
}

function listFiles(root) {
  const out = [];
  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else out.push(path.relative(root, full));
    }
  }
  walk(root);
  return out.sort();
}

async function captureErrors(fn) {
  const lines = [];
  const orig = console.error;
  console.error = (...args) => {
    const line = args.map(String).join(" ");
    lines.push(line);
    orig.call(console, line);
  };
  try {
    return { result: await fn(), lines };
  } finally {
    console.error = orig;
  }
}

function importLoader(loaderFile) {
  return import(pathToFileURL(loaderFile).href + "?t=" + Date.now() + Math.random());
}

after(() => {
  for (const dir of fixtures) {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

describe("production loader registration", () => {
  test("adds absolute category skill paths once across two hook applications", async () => {
    const root = makeRoot("opencode-loader-");
    copyCoreSkills(root);
    writeSkill(
      path.join(root, "plugins", "misc", "skills", "kept-skill"),
      skillDoc("kept-skill", "kept"),
    );
    const loaderFile = writeLoader(root);
    const mod = await importLoader(loaderFile);
    const hooks = await mod.default();
    const config = { skills: { paths: [] }, command: { keep: { template: "KEEP" } } };
    await hooks.config(config);
    await hooks.config(config);

    const expected = [
      fs.realpathSync(path.join(root, "plugins", "core", "skills")),
      fs.realpathSync(path.join(root, "plugins", "misc", "skills")),
    ];
    assert.deepEqual(
      config.skills.paths.map((p) => fs.realpathSync(p)),
      expected,
    );
    assert.equal(config.skills.paths.every((p) => path.isAbsolute(p)), true);
    assert.deepEqual(config.command, { keep: { template: "KEEP" } });
  });

  test("registers all 15 repository category skill paths from the production checkout", async () => {
    const mod = await importLoader(productionLoader);
    const hooks = await mod.default();
    const config = { skills: { paths: [] } };
    await hooks.config(config);
    await hooks.config(config);

    const categories = fs
      .readdirSync(path.join(repoRoot, "plugins"))
      .filter((name) => fs.statSync(path.join(repoRoot, "plugins", name)).isDirectory())
      .sort();
    assert.equal(categories.length, 15);
    const expected = categories.map((name) =>
      fs.realpathSync(path.join(repoRoot, "plugins", name, "skills")),
    );
    assert.deepEqual(
      config.skills.paths.map((p) => fs.realpathSync(p)),
      expected,
    );
  });
});

describe("sorted absolute paths and path spaces", () => {
  test("resolves a fixture directory that contains a space and sorts skill paths", async () => {
    const parent = makeRoot("opencode-space-");
    const root = path.join(parent, "path with space");
    fs.mkdirSync(root, { recursive: true });
    writeSkill(
      path.join(root, "plugins", "zeta", "skills", "zeta-skill"),
      skillDoc("zeta-skill", "zeta"),
    );
    writeSkill(
      path.join(root, "plugins", "alpha", "skills", "alpha-skill"),
      skillDoc("alpha-skill", "alpha"),
    );
    const loaderFile = writeLoader(root);
    const mod = await importLoader(loaderFile);
    const hooks = await mod.default();
    const config = { skills: { paths: [] } };
    await hooks.config(config);

    const expected = [
      fs.realpathSync(path.join(root, "plugins", "alpha", "skills")),
      fs.realpathSync(path.join(root, "plugins", "zeta", "skills")),
    ];
    assert.deepEqual(
      config.skills.paths.map((p) => fs.realpathSync(p)),
      expected,
    );
    assert.equal(path.isAbsolute(config.skills.paths[0]), true);
  });
});

describe("missing directory", () => {
  test("skips a missing skills directory with one diagnostic and still loads other paths", async () => {
    const root = makeRoot("opencode-missing-");
    writeSkill(
      path.join(root, "plugins", "core", "skills", "kept-skill"),
      skillDoc("kept-skill", "kept"),
    );
    fs.mkdirSync(path.join(root, "plugins", "hollow"), { recursive: true });
    const missing = path.join(root, "plugins", "hollow", "skills");
    const loaderFile = writeLoader(root);
    const mod = await importLoader(loaderFile);
    const captured = await captureErrors(async () => {
      const hooks = await mod.default();
      const config = { skills: { paths: [] } };
      await hooks.config(config);
      return config.skills.paths;
    });
    const diagnostic = "majestic-abilities: missing skills directory: " + missing;
    assert.equal(captured.lines.filter((line) => line === diagnostic).length, 1);
    assert.equal(captured.result.length, 1);
    assert.equal(
      fs.realpathSync(captured.result[0]),
      fs.realpathSync(path.join(root, "plugins", "core", "skills")),
    );
  });

  test("reports one diagnostic when the plugins root is absent", async () => {
    const root = makeRoot("opencode-no-plugins-");
    const pluginsDir = path.join(root, "plugins");
    const loaderFile = writeLoader(root);
    const mod = await importLoader(loaderFile);
    const captured = await captureErrors(async () => {
      const hooks = await mod.default();
      const config = { skills: { paths: ["keep-me"] } };
      await hooks.config(config);
      return config;
    });
    const diagnostic = "majestic-abilities: missing repository path: " + pluginsDir;
    assert.equal(captured.lines.filter((line) => line === diagnostic).length, 1);
    assert.deepEqual(captured.result.skills.paths, ["keep-me"]);
  });
});

describe("symlink escape", () => {
  test("rejects a skills directory symlink that resolves outside plugins/", async () => {
    const root = makeRoot("opencode-escape-");
    const outside = path.join(root, "outside-skills");
    writeSkill(path.join(outside, "escaped-skill"), skillDoc("escaped-skill", "outside"));
    fs.mkdirSync(path.join(root, "plugins", "core"), { recursive: true });
    fs.symlinkSync(outside, path.join(root, "plugins", "core", "skills"));
    const loaderFile = writeLoader(root);
    const mod = await importLoader(loaderFile);
    const escaped = fs.realpathSync(outside);
    const captured = await captureErrors(async () => {
      const hooks = await mod.default();
      const config = { skills: { paths: [] } };
      await hooks.config(config);
      return config.skills.paths;
    });
    assert.equal(captured.lines.some((line) => line.includes("escaping path:")), true);
    assert.equal(captured.lines.some((line) => line.includes(escaped)), true);
    assert.deepEqual(captured.result, []);
  });

  test("rejects a plugins root symlink that escapes the checkout", async () => {
    const parent = makeRoot("opencode-plugins-escape-");
    const root = path.join(parent, "checkout");
    const outside = path.join(parent, "outside-plugins");
    fs.mkdirSync(root, { recursive: true });
    writeSkill(
      path.join(outside, "evil", "skills", "escaped-skill"),
      skillDoc("escaped-skill", "MARKER_OUTSIDE_CONTENT"),
    );
    fs.symlinkSync(outside, path.join(root, "plugins"));
    const loaderFile = writeLoader(root);
    const mod = await importLoader(loaderFile);
    const escaped = fs.realpathSync(outside);
    const captured = await captureErrors(async () => {
      const hooks = await mod.default();
      const config = { skills: { paths: [] } };
      await hooks.config(config);
      return config.skills.paths;
    });
    assert.equal(captured.lines.some((line) => line.includes("escaping path:")), true);
    assert.equal(captured.lines.some((line) => line.includes(escaped)), true);
    assert.equal(captured.lines.some((line) => line.includes("MARKER_OUTSIDE_CONTENT")), false);
    assert.deepEqual(captured.result, []);
  });

  test("rejects a category root symlink that escapes plugins/", async () => {
    const root = makeRoot("opencode-category-escape-");
    const outside = path.join(root, "outside-category");
    writeSkill(
      path.join(outside, "skills", "escaped-skill"),
      skillDoc("escaped-skill", "MARKER_CATEGORY_ESCAPE"),
    );
    fs.mkdirSync(path.join(root, "plugins"), { recursive: true });
    fs.symlinkSync(outside, path.join(root, "plugins", "core"));
    const loaderFile = writeLoader(root);
    const mod = await importLoader(loaderFile);
    const escaped = fs.realpathSync(outside);
    const captured = await captureErrors(async () => {
      const hooks = await mod.default();
      const config = { skills: { paths: [] } };
      await hooks.config(config);
      return config.skills.paths;
    });
    assert.equal(captured.lines.some((line) => line.includes("escaping path:")), true);
    assert.equal(captured.lines.some((line) => line.includes(escaped)), true);
    assert.equal(captured.lines.some((line) => line.includes("MARKER_CATEGORY_ESCAPE")), false);
    assert.deepEqual(captured.result, []);
  });
});

describe("project and user absolute symlinks", () => {
  test("resolves checkout root through absolute project and user loader symlinks", async () => {
    const checkout = makeRoot("opencode-symlink-checkout-");
    const home = makeRoot("opencode-symlink-home-");
    const project = makeRoot("opencode-symlink-project-");
    copyCoreSkills(checkout);
    const loaderFile = writeLoader(checkout);
    const absLoader = fs.realpathSync(loaderFile);

    const userSymlink = path.join(home, ".config", "opencode", "plugins", "majestic-abilities.js");
    const projectSymlink = path.join(project, ".opencode", "plugins", "majestic-abilities.js");
    fs.mkdirSync(path.dirname(userSymlink), { recursive: true });
    fs.mkdirSync(path.dirname(projectSymlink), { recursive: true });
    fs.symlinkSync(absLoader, userSymlink);
    fs.symlinkSync(absLoader, projectSymlink);

    for (const [label, symlink] of [
      ["user", userSymlink],
      ["project", projectSymlink],
    ]) {
      assert.equal(fs.lstatSync(symlink).isSymbolicLink(), true);
      assert.equal(path.isAbsolute(fs.readlinkSync(symlink)), true);
      assert.equal(fs.realpathSync(symlink), absLoader);
      const mod = await importLoader(symlink);
      const hooks = await mod.default();
      const config = { skills: { paths: [] } };
      await hooks.config(config);
      assert.equal(
        fs.realpathSync(config.skills.paths[0]),
        fs.realpathSync(path.join(checkout, "plugins", "core", "skills")),
        label + " route",
      );
    }
  });
});

describe("no writes at runtime", () => {
  test("creates nothing new in the fixture or the repository", async () => {
    const root = makeRoot("opencode-nowrite-");
    copyCoreSkills(root);
    const loaderFile = writeLoader(root);
    const beforeFiles = listFiles(root);
    const beforeRepo = execSync("git status --porcelain", { cwd: repoRoot, encoding: "utf8" });
    const mod = await importLoader(loaderFile);
    const hooks = await mod.default();
    const config = { skills: { paths: [] } };
    await hooks.config(config);
    await hooks.config(config);
    const afterFiles = listFiles(root);
    const afterRepo = execSync("git status --porcelain", { cwd: repoRoot, encoding: "utf8" });
    assert.deepEqual(afterFiles, beforeFiles);
    assert.equal(afterRepo, beforeRepo);
    const adapterSkills = listFiles(path.join(root, ".opencode")).filter((f) =>
      f.endsWith("SKILL.md"),
    );
    assert.deepEqual(adapterSkills, []);
  });
});
