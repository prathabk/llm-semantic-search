/**
 * JSON Formatter with Syntax Highlighting
 * Formats JSON with proper indentation, colors, and collapsible sections
 */

class JSONFormatter {
    constructor(options = {}) {
        this.options = {
            indent: options.indent || 2,
            collapsible: options.collapsible !== false,
            ...options
        };
    }

    /**
     * Format JSON object/string into HTML with syntax highlighting
     * @param {Object|String} data - JSON data to format
     * @returns {String} - HTML string with formatted JSON
     */
    format(data) {
        let jsonObj;

        // Parse if string
        if (typeof data === 'string') {
            try {
                jsonObj = JSON.parse(data);
            } catch (e) {
                return `<span class="json-error">Invalid JSON: ${e.message}</span>`;
            }
        } else {
            jsonObj = data;
        }

        return this.formatValue(jsonObj, 0);
    }

    formatValue(value, depth) {
        if (value === null) {
            return '<span class="json-null">null</span>';
        }

        if (value === undefined) {
            return '<span class="json-undefined">undefined</span>';
        }

        const type = typeof value;

        if (type === 'boolean') {
            return `<span class="json-boolean">${value}</span>`;
        }

        if (type === 'number') {
            return `<span class="json-number">${value}</span>`;
        }

        if (type === 'string') {
            return `<span class="json-string">"${this.escapeHtml(value)}"</span>`;
        }

        if (Array.isArray(value)) {
            return this.formatArray(value, depth);
        }

        if (type === 'object') {
            return this.formatObject(value, depth);
        }

        return String(value);
    }

    formatObject(obj, depth) {
        const keys = Object.keys(obj);

        if (keys.length === 0) {
            return '<span class="json-punctuation">{}</span>';
        }

        const indent = '  '.repeat(depth);
        const nextIndent = '  '.repeat(depth + 1);

        let html = '<span class="json-punctuation">{</span>';

        if (this.options.collapsible && depth > 0) {
            html = `<span class="json-collapse" onclick="toggleCollapse(this)">▼</span>${html}`;
        }

        html += '\n';

        keys.forEach((key, index) => {
            const value = obj[key];
            const isLast = index === keys.length - 1;

            html += `${nextIndent}<span class="json-key">"${this.escapeHtml(key)}"</span><span class="json-punctuation">: </span>`;
            html += this.formatValue(value, depth + 1);

            if (!isLast) {
                html += '<span class="json-punctuation">,</span>';
            }

            html += '\n';
        });

        html += `${indent}<span class="json-punctuation">}</span>`;

        return html;
    }

    formatArray(arr, depth) {
        if (arr.length === 0) {
            return '<span class="json-punctuation">[]</span>';
        }

        const indent = '  '.repeat(depth);
        const nextIndent = '  '.repeat(depth + 1);

        let html = '<span class="json-punctuation">[</span>';

        if (this.options.collapsible && depth > 0) {
            html = `<span class="json-collapse" onclick="toggleCollapse(this)">▼</span>${html}`;
        }

        html += '\n';

        arr.forEach((item, index) => {
            const isLast = index === arr.length - 1;

            html += nextIndent;
            html += this.formatValue(item, depth + 1);

            if (!isLast) {
                html += '<span class="json-punctuation">,</span>';
            }

            html += '\n';
        });

        html += `${indent}<span class="json-punctuation">]</span>`;

        return html;
    }

    escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
}

// Toggle collapse/expand for collapsible sections
function toggleCollapse(element) {
    const parent = element.parentElement;
    const content = parent.querySelector('.json-content');

    if (element.textContent === '▼') {
        element.textContent = '▶';
        if (content) content.style.display = 'none';
    } else {
        element.textContent = '▼';
        if (content) content.style.display = 'block';
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = JSONFormatter;
}
