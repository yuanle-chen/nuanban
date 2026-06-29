let speechEnabled = true

export function setSpeechEnabled(enabled: boolean) {
  speechEnabled = enabled
}

export function isSpeechEnabled() {
  return speechEnabled
}

export function speak(text: string, options?: { rate?: number; pitch?: number; volume?: number }) {
  if (!speechEnabled) return
  if (!window.speechSynthesis) {
    console.warn('浏览器不支持语音合成')
    return
  }

  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'zh-CN'
  utterance.rate = options?.rate ?? 0.9
  utterance.pitch = options?.pitch ?? 1
  utterance.volume = options?.volume ?? 1

  window.speechSynthesis.speak(utterance)
}

export function stopSpeaking() {
  if (window.speechSynthesis) {
    window.speechSynthesis.cancel()
  }
}

export function isSpeaking() {
  return window.speechSynthesis?.speaking ?? false
}
