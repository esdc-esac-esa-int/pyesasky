// What is this? Check this url:
// http://stackoverflow.com/questions/2061339/ignore-firebug-console-when-not-installed
if (!window.console || !console.firebug) {
	var names = [ "log", "debug", "info", "warn", "error", "assert", "dir",
			"dirxml", "group", "groupEnd", "time", "timeEnd", "count", "trace",
			"profile", "profileEnd" ];
	window.console = {};
	for ( var i = 0; i < names.length; ++i)
		window.console[names[i]] = function() {
		}
}