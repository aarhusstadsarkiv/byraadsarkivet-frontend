function loadScript(src, callback) {
    var script = document.createElement('script');
    script.type = 'text/javascript';

    // IE
    if (script.readyState) {
        script.onreadystatechange = function () {
            if (script.readyState === 'loaded' || script.readyState === 'complete') {
                script.onreadystatechange = null;
                callback();
            }
        }
    }
    // Others
    else {
        script.onload = callback;
    }

    script.src = src;
    script.async = true;
    console.log("Loading script...");
    document.body.appendChild(script);
}


function mySetCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString() + "; ";
    var rest = "samesite=lax; secure=true;"
    document.cookie = cname + "=" + cvalue + ";" + expires + rest;
}

function removeCookie(name) {
    document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; ";
    console.log("removing cookie...");
}


window.addEventListener('load', function() {
    const analytics = "https://siteimproveanalytics.com/js/siteanalyze_2240844.js";
    window.cookieconsent.initialise({
        revokeBtn: "<div id='cc-revoke-btn' class='cc-revoke'></div>",
        type: "opt-in",
        position: "bottom-right",
        animateRevocable: false,
        palette: {
            "popup": {
                "background": "#3661d8" // "#237afc" // "#3661d8"
            },
            "button": {
                "background": "#fff", // #333
                "text": "#3661d8" // "#237afc"
            }
        },
        content: {
            "message": '<p>Byrådsarkivet vil gerne bruge en cookie til at føre besøgsstatistik.</p> \
            <p>Du kan altid ændre dit valg ved at klikke på "Valg af cookies"-linket nederst på hver side.</p>',
            "allow": 'Tillad cookie',
            "deny": 'Nej tak',
            "link": 'Læs mere i vores cookiepolitik',
            "href": '/cookies',
            "policy": 'Cookies',
            "target": '_blank',
        },
        onInitialise: function(status) {
            // Always runs on load and reload
            console.log("Cookieconsent initialized");
            if (document.cookie.indexOf('cookieconsent_status=allow') > -1) {
                console.log("Allowed as per document.cookie");
                if (!window._sz) {
                    loadScript(analytics);
                }
            } else if (document.cookie.indexOf('cookieconsent_status=deny') > -1) {
                console.log("Denied as per document.cookie");
                // if (window._sz) removeScript(analytics);
                if (document.cookie.indexOf('__cfduid') > -1) {
                    removeCookie('__cfduid');
                }
            } else {
                console.log("Cookie-choice not yet made as per document.cookie");
            }
        },
        onStatusChange: function(status, chosenBefore) {
            window.location.reload();
        }
    });
    // Remove original cc-revoke-div
    let originalRevokeBtn = document.querySelector("#cc-revoke-btn");
    if (originalRevokeBtn) {
        originalRevokeBtn.parentElement.removeChild(originalRevokeBtn);
    }
    // Add revokeBtn-funtionality from footer-link
    // Original revokeBtn is hidden with css in cookieconsent.css
    let revokeBtn = document.querySelector("#revokebutton");
    if (revokeBtn) {
        revokeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            let ccWindow = document.querySelector(".cc-window");
            ccWindow.style.display = "flex";
            ccWindow.classList.remove("cc-invisible");
        })
    }
});
