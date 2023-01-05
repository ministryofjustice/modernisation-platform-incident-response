import { nodeListForEach } from 'govuk-frontend/govuk/common'
import Actions from './action.js'

function initAll() {
    const $actions = document.querySelectorAll('[data-module="app-actions"]');
    nodeListForEach($actions, ($el) => {
        new Actions($el).init();
    })
}

export { initAll, Actions }
