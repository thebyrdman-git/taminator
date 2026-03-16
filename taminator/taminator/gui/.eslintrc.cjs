module.exports = {
  root: true,
  env: { node: true, es2022: true },
  parserOptions: { ecmaVersion: 2022, sourceType: 'script' },
  extends: ['eslint:recommended'],
  ignorePatterns: ['dist/', 'out/', 'node_modules/', '*.min.js'],
  overrides: [
    {
      files: ['**/*.js'],
      rules: {
        'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
        'no-console': 'off'
      }
    }
  ]
};
