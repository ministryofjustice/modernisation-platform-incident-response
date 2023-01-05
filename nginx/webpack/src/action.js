import { nodeListForEach } from 'govuk-frontend/govuk/common'
import api from './lib/api';

function Actions ($module) {
  this.$module = $module;
  this.incidentId = $module.getAttribute('data-incident-id');
  this.$actions = $module.querySelectorAll('input[type="checkbox"]');
  this.$actionLabels = $module.querySelectorAll('label');
}

Actions.prototype.init = function init() {
  nodeListForEach(this.$actions, $action => {
    $action.addEventListener('change', this.handleCheck.bind(this));
  });
  nodeListForEach(this.$actionLabels, $action => {
    $action.addEventListener('click', this.handleClickLabel.bind(this));
  });
}

Actions.prototype.handleCheck = function handleCheck(event) {
  const actionId = event.target.value;

  const form = new FormData();
  form.set('done', event.target.checked);
  form.set('done_date', event.target.checked ? (new Date()).toISOString() : '');

  api('PATCH', `/incidents/${this.incidentId}/actions/${actionId}/`, form);
}

Actions.prototype.handleClickLabel = function handleClickLabel(event) {
  if (event.target.tagName !== 'LABEL') return;

  event.preventDefault();
  event.stopPropagation();

  const checkbox = document.getElementById(event.target.getAttribute('for'));
  const actionId = checkbox.value;

  const description = prompt('Enter a new action description\n\nTag a user with <@SlackIdOrName>', event.target.getAttribute('data-raw'));

  if (description) {
    const form = new FormData();
    form.set('details', description);

    api('PATCH', `/incidents/${this.incidentId}/actions/${actionId}/`, form).then(() => {
      window.location.reload();
    })
  }
}

export default Actions;
