import type { Plugin } from 'vite'

export function fixHtmlEncoding(): Plugin {
  return {
    name: 'fix-html-encoding',
    apply: 'build',
    // Use Rollup's generateBundle hook to mutate HTML assets safely
    generateBundle(_options, bundle) {
      for (const [fileName, output] of Object.entries(bundle)) {
        if (fileName.endsWith('.html') && output.type === 'asset') {
          let source = typeof output.source === 'string'
            ? output.source
            : output.source?.toString() ?? ''

          // Ensure charset meta exists to avoid encoding issues
          if (!/charset\s*=\s*utf-8/i.test(source)) {
            source = source.replace(
              /<head>/i,
              '<head><meta charset="utf-8">'
            )
          }

          // Normalize common mis-encoded characters if any (best-effort)
          // You can add specific replacements here if needed
          output.source = source
        }
      }
    },
  }
}
