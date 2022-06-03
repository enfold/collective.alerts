process.traceDeprecation = true;
const package_json = require("./package.json");
const path = require("path");
const patternslib_config = require("@patternslib/patternslib/webpack/webpack.config");
const mf_config = require("@patternslib/patternslib/webpack/webpack.mf");

module.exports = (env, argv) => {
    let config = {
        entry: {
            "jsalerts.min": path.resolve(__dirname, "resources/index.js"),
        }
    };

    config = patternslib_config(env, argv, config, ["jsalerts.min"]);

    config.output.path = path.resolve(__dirname, "src/collective/alerts/browser/static");

    config.plugins.push(
        mf_config({
            package_json: package_json,
            remote_entry: config.entry["jsalerts.min"],
        })
    );

    return config;
};
