if (!self.define) {
    let e, s = {};
    const i = (i, n) => (
        i = new URL(i + ".js", n).href,
        s[i] || new Promise((s => {
            if ("document" in self) {
                const e = document.createElement("script");
                e.src = i;
                e.onload = s;
                document.head.appendChild(e);
            } else {
                e = i;
                importScripts(i);
                s();
            }
        })).then(() => {
            let e = s[i];
            if (!e) throw new Error(`Module ${i} didn’t register its module`);
            return e;
        })
    );
    self.define = (n, r) => {
        const o = e || ("document" in self ? document.currentScript.src : "") || location.href;
        if (s[o]) return;
        let t = {};
        const l = e => i(e, o),
            a = {
                module: { uri: o },
                exports: t,
                require: l
            };
        s[o] = Promise.all(n.map(e => a[e] || l(e))).then(e => (r(...e), t));
    };
}

define(["./workbox-1504e367"], function (e) {
    "use strict";
    self.skipWaiting();
    e.clientsClaim();
    e.precacheAndRoute([
        { url: "assets/DowntimeCard.vue_vue_type_script_setup_true_lang-BsQsdFae.js", revision: null },
        { url: "assets/index-Cz8wn0fu.css", revision: null },
        { url: "assets/index-D6nZG9GM.js", revision: null },
        { url: "assets/OrderDetails-Bvl0OLix.js", revision: null },
        { url: "assets/workbox-window.prod.es5-fJwV-9vL.js", revision: null },
        { url: "assets/WorkstationDetails-mnYAFyRX.js", revision: null },
        { url: "assets/WorkstationList-B4gLi1a5.js", revision: null },
        { url: "index.html", revision: "8ad4ba9d010ce7568dcfed5077317dcd" },
        { url: "icons/pwa-192x192.png", revision: "7a596c431a49b90e96df14be23e350ae" },
        { url: "icons/pwa-512x512.png", revision: "29a00308d1bc32f737db2b69a6e17cc5" },
        { url: "icons/pwa-maskable-192x192.png", revision: "f59aaf29f4d97e375fda4ec6a95a1583" },
        { url: "icons/pwa-maskable-512x512.png", revision: "13202fd69b9b15c33feb0dfd26997b70" },
        { url: "manifest.webmanifest", revision: "53b2f331b87afdb05e9018faacf6626b" }
    ], {});
    e.cleanupOutdatedCaches();
    e.registerRoute(new e.NavigationRoute(e.createHandlerBoundToURL("index.html")));
    e.registerRoute(
        /^https:\/\/jsonplaceholder\.typicode\.com\/.*/i,
        new e.NetworkFirst({ cacheName: "api-cache", plugins: [] }),
        "GET"
    );
});
