process.traceDeprecation = true;
const mf_config = require("@patternslib/dev/webpack/webpack.mf");
const path = require("path");
const package_json = require("./package.json");
const package_json_mockup = require("@plone/mockup/package.json");
const package_json_patternslib = require("@patternslib/patternslib/package.json");
const patternslib_config = require("@patternslib/dev/webpack/webpack.config.js");

module.exports = (env, argv) => {
    let config = {
        entry: {
            "jsalerts.min": path.resolve(__dirname, "resources/index.js"),
        }
    };

    config = patternslib_config(env, argv, config, ["@plone/mockup"]);
    config.output.path = path.resolve(__dirname, "src/collective/alerts/browser/static");

    config.plugins.push(
        mf_config({
            name: "jsalerts",
            filename: "jsalerts-remote.min.js",
            remote_entry: config.entry["jsalerts.min"],
            dependencies: {
                ...package_json_patternslib.dependencies,
                ...package_json_mockup.dependencies,
                ...package_json.dependencies,
            },
        })
    );

    return config;
};
