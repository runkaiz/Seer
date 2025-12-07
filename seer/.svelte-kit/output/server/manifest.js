export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["robots.txt"]),
	mimeTypes: {".txt":"text/plain"},
	_: {
		client: {start:"_app/immutable/entry/start.BSrqmx14.js",app:"_app/immutable/entry/app.B8EYTysr.js",imports:["_app/immutable/entry/start.BSrqmx14.js","_app/immutable/chunks/B54vnEzH.js","_app/immutable/chunks/DQYrmzXI.js","_app/immutable/chunks/ziqNh-sv.js","_app/immutable/entry/app.B8EYTysr.js","_app/immutable/chunks/DQYrmzXI.js","_app/immutable/chunks/BqevFqEi.js","_app/immutable/chunks/DQzTVXwp.js","_app/immutable/chunks/ziqNh-sv.js","_app/immutable/chunks/DdIbhXnm.js","_app/immutable/chunks/BKWbP05J.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:true},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js'))
		],
		remotes: {
			
		},
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
