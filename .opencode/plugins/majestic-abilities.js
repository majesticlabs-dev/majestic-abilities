import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

function isInside(child, parent) {
  return child === parent || child.startsWith(parent + path.sep);
}

function diagnose(message) {
  console.error("majestic-abilities: " + message);
}

function loadSkillPaths(checkoutRoot) {
  const checkoutReal = fs.realpathSync(checkoutRoot);
  const pluginsDir = path.join(checkoutRoot, "plugins");
  const skillPaths = [];

  let pluginsRoot;
  try {
    if (!fs.existsSync(pluginsDir)) {
      diagnose("missing repository path: " + pluginsDir);
      return skillPaths;
    }
    pluginsRoot = fs.realpathSync(pluginsDir);
  } catch {
    diagnose("missing repository path: " + pluginsDir);
    return skillPaths;
  }

  if (!isInside(pluginsRoot, checkoutReal)) {
    diagnose("escaping path: " + pluginsRoot);
    return skillPaths;
  }

  let categories = [];
  try {
    categories = fs.readdirSync(pluginsDir).sort();
  } catch {
    diagnose("missing repository path: " + pluginsDir);
    return skillPaths;
  }

  for (const category of categories) {
    const categoryDir = path.join(pluginsDir, category);
    let categoryReal;
    try {
      const st = fs.lstatSync(categoryDir);
      if (!st.isDirectory() && !st.isSymbolicLink()) continue;
      categoryReal = fs.realpathSync(categoryDir);
    } catch {
      continue;
    }
    if (!isInside(categoryReal, pluginsRoot)) {
      diagnose("escaping path: " + categoryReal);
      continue;
    }
    let st;
    try {
      st = fs.statSync(categoryDir);
    } catch {
      continue;
    }
    if (!st.isDirectory()) continue;

    const skillsDir = path.join(categoryDir, "skills");
    if (!fs.existsSync(skillsDir)) {
      diagnose("missing skills directory: " + skillsDir);
      continue;
    }
    let resolvedSkills;
    try {
      resolvedSkills = fs.realpathSync(skillsDir);
    } catch {
      diagnose("escaping path: " + skillsDir);
      continue;
    }
    if (!isInside(resolvedSkills, pluginsRoot)) {
      diagnose("escaping path: " + resolvedSkills);
      continue;
    }
    skillPaths.push(resolvedSkills);
  }
  return skillPaths;
}

export default async function majesticAbilitiesPlugin() {
  const loaderFile = fs.realpathSync(fileURLToPath(import.meta.url));
  const checkoutRoot = fs.realpathSync(path.resolve(path.dirname(loaderFile), "../.."));
  const skillPaths = loadSkillPaths(checkoutRoot);
  return {
    config: async function applyConfig(config) {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      for (const skillPath of skillPaths) {
        const found = config.skills.paths.some(function (existing) {
          try {
            return fs.realpathSync(existing) === skillPath;
          } catch {
            return path.resolve(existing) === skillPath;
          }
        });
        if (!found) config.skills.paths.push(skillPath);
      }
    },
  };
}
