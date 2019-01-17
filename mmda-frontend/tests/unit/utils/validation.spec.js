import rules from '@/utils/validation.js'

describe('Email rules', () => {
  it('validate correct email', () => {
    expect(rules.email('foo@bar.de')).toBe(true)
  })

  it('validate invalid email', () => {
    expect(rules.email('foo')).toMatch('Invalid e-mail')
  })

  it('validate invalid email', () => {
    expect(rules.email('foo@')).toMatch('Invalid e-mail')
  })
})

describe('Alphanum ruless', () => {
  it('validate correct string', () => {
    expect(rules.alphanum('happystring')).toBe(true)
    expect(rules.alphanum('VERYHAPPY')).toBe(true)
  })

  it('validate invalid string', () => {
    expect(rules.alphanum('badstring!!!!')).toBe('Invalid characters.')
    expect(rules.alphanum('(&$*)  !!!!')).toBe('Invalid characters.')
  })
})
