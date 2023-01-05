import getCookie from "./getCookie";

export default function api(method, path, body = null, config = {}) {
  const csrftoken = getCookie('csrftoken');

  return fetch(`/core${path}`, Object.assign({
      method,
      mode: 'same-origin',
      body,
      headers: {
          'X-CSRFToken': csrftoken
      }
  }, config));
}
