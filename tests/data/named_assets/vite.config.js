import path from 'node:path';

export default {
  build: {
    manifest: 'manifest.json',
    rollupOptions: {
      input: {
        'one': path.resolve('./one.js'),
      },
    },
  },
};
