// String/Input validation
// Used in v-form
// https://vuetifyjs.com/en/components/forms#creating-rules

const rules = {
  alphanum: value => {
    const pattern = /^[a-zA-Z0-9]+$/i
    return pattern.test(value) || 'Invalid characters.'
  },
  required: value => !!value || 'Required.',
  counter: value => value.length <= 64 || 'Max 64 characters.',
  minlength8: value => value.length >= 8 || 'Min 8 characters.',
  email: value => {
    const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return pattern.test(value) || 'Invalid e-mail.'
  }
}

export default rules
