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

describe('Alphanum rules', () => {
  it('validate correct string', () => {
    expect(rules.alphanum('happystring')).toBe(true)
    expect(rules.alphanum('VERYHAPPY')).toBe(true)
  })

  it('validate invalid string', () => {
    expect(rules.alphanum('badstring!!!!')).toMatch('Invalid characters.')
    expect(rules.alphanum('(&$*)  !!!!')).toMatch('Invalid characters.')
  })
})

describe('Max and min length rules', () => {
  it('validate max min length', () => {
    expect(rules.counter('thisisok')).toBe(true)
    expect(rules.counter('thisnooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooot')).toMatch('Max 64 characters.')
  })

  it('validate invalid max min length', () => {
    expect(rules.minlength8('muchbetter')).toBe(true)
    expect(rules.minlength8('not')).toMatch('Min 8 characters.')
  })
})
