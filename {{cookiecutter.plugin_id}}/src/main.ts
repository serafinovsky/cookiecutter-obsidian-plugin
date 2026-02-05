import { Plugin, moment } from "obsidian";
{% if cookiecutter.enable_i18n == "yes" -%}
import { t, initI18n } from "./i18n";
{% endif %}

export default class PluginMain extends Plugin {
  async onload() {
    {% if cookiecutter.enable_i18n == "yes" -%}
    const userLocale = moment.locale();
    await initI18n(userLocale);
    // eslint-disable-next-line no-console
    console.log(t("plugin_loaded")); 
    {% else -%}
    console.log("{{cookiecutter.plugin_name}} loaded");
    {% endif %}
  }

  onunload() {
    // eslint-disable-next-line no-console
    console.log("{{cookiecutter.plugin_name}} unloaded");
  }
}
