import path from 'node:path';
import { fileURLToPath } from 'node:url';

const PLUGIN_DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILLS_DIR = path.resolve(PLUGIN_DIR, '../../skills');

const ACTIVATION_NOTICE = `hexis is active. Full workflow skills are loaded.
Start with: hexis:dispatch`;

const INJECTION_GUARD = 'hexis:bootstrap';

function registerSkillsDir(config) {
  const existingPaths = config.skills?.paths ?? [];
  if (existingPaths.includes(SKILLS_DIR)) return;
  config.skills = {
    ...config.skills,
    paths: [...existingPaths, SKILLS_DIR],
  };
}

function injectActivationNotice(messages) {
  if (!messages.length) return;
  const firstUserMessage = messages.find(m => m.info.role === 'user');
  if (!firstUserMessage?.parts.length) return;
  const alreadyInjected = firstUserMessage.parts.some(
    p => p.type === 'text' && p.text.includes(INJECTION_GUARD)
  );
  if (alreadyInjected) return;
  const [firstPart] = firstUserMessage.parts;
  const noticePart = { ...firstPart, type: 'text', text: `<!-- ${INJECTION_GUARD} -->\n${ACTIVATION_NOTICE}` };
  firstUserMessage.parts = [noticePart, ...firstUserMessage.parts];
}

export const HexisPlugin = async () => ({
  config: async (config) => registerSkillsDir(config),
  'experimental.chat.messages.transform': async (_input, output) => injectActivationNotice(output.messages),
});
