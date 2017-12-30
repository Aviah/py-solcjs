const fs = require('fs');
config = JSON.parse(fs.readFileSync(process.env.HOME + '/.py_solcjs/config.json'));
releases = JSON.parse(fs.readFileSync(process.env.HOME + '/.py_solcjs/solcjs_releases.json'));

if(typeof version == 'undefined'){
    if (process.env.PY_SOLCJS_COMPILATION_VERSION) {
        version = process.env.PY_SOLCJS_COMPILATION_VERSION;
    } else {
        version = config['defaultCompilationVersion'];
    }
}

solcjsPath = config["solcjsNodeModulePath"][process.platform];
soljson = config["soljsonVersionsDir"] + "/" + releases[version];

var solc = require(solcjsPath);
var solc = solc.setupMethods(require(soljson));
var compiled = solc.compileStandardWrapper(JSON.stringify(input_json));
console.log(compiled);
