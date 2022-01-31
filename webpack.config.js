process.traceDeprecation = true;
const path = require("path");
const patternslib_config = require("@patternslib/patternslib/webpack/webpack.config");

module.exports = async (env, argv) => {
    let config = {
        entry: {
            "jsalerts": path.resolve(__dirname, "resources/jsalerts-config"),
        },
	externals: {
            window: "window",
            $: 'jquery',
            jquery: 'jQuery',
            "window.jquery": 'jQuery',
        },
    };
    config = patternslib_config(env, argv, config, ["mockup"]);

    config.output.path = path.resolve(__dirname, "src/collective/alerts/browser/static");

    return config;
};
