import i18next from "i18next";
import en from "../../locales/en.json";

const locales = {
  en
};

type Locale = keyof typeof locales;
type TranslationParams = Record<string, string | number>;

/**
 * Initialize the i18n system
 * @param locale - initial locale (defaults to 'en')
 */
export async function initI18n(locale: string = "en") {
  await i18next.init({
    lng: locale,
    fallbackLng: "en",
    resources: {
      en: { translation: en }
    },
    interpolation: {
      escapeValue: false
    }
  });
}

/**
 * Change the current language
 * @param locale - language code (e.g., 'en', 'ru')
 */
export async function setLocale(locale: string): Promise<void> {
  if (locale in locales) {
    await i18next.changeLanguage(locale);
  }
}

/**
 * Get translation for a key
 * @param key - translation key
 * @param params - interpolation parameters (optional)
 * 
 * @example
 * // Simple translation
 * t("plugin_loaded")
 * 
 * @example
 * // With interpolation (see docs for details)
 * t("greeting", { name: "John" })
 * 
 * @example
 * // With pluralization (see docs for details)
 * t("file", { count: 5 })
 */
export function t(key: string, params?: TranslationParams): string {
  return i18next.t(key, params);
}

/**
 * Get list of available locales
 */
export function getAvailableLocales(): Locale[] {
  return Object.keys(locales) as Locale[];
}

/**
 * Get current locale
 */
export function getCurrentLocale(): string {
  return i18next.language;
}
