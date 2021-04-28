$(document).ready(function() {

    
    function compareValues(key, order = 'asc') {
        return function innerSort(a, b) {
            if (!a.hasOwnProperty(key) || !b.hasOwnProperty(key)) {
                // property doesn't exist on either object
                return 0;
            }
        
            const varA = (typeof a[key] === 'string')
                ? a[key].toUpperCase() : a[key];
            const varB = (typeof b[key] === 'string')
                ? b[key].toUpperCase() : b[key];
        
            let comparison = 0;
            if (varA > varB) {
                comparison = 1;
            } else if (varA < varB) {
                comparison = -1;
            }
            return (
                (order === 'desc') ? (comparison * -1) : comparison
            );
        };
    }

    function localize(date) {
        var months = {
            "01": "januar",
            "02": "februar",
            "03": "marts",
            "04": "april",
            "05": "maj",
            "06": "juni",
            "07": "juli",
            "08": "august",
            "09": "september",
            "10": "oktober",
            "11": "november",
            "12": "december"
        };
        var day = date.slice(8);
        var month = months[date.slice(5,7)];
        var year = date.slice(0,4);
        return day + ". " + month + " " + year;
    }

    function fetchAgendaItem(id) {
        var current_meeting = window.location.pathname.split('/').slice(-1)[0];
        var db_url = window.location.pathname.split("/")[1];

        $.ajax({
            dataType: "json",
            url: "/" + db_url + "/cases/" + id + ".json?_shape=objects&_json=fora&_json=decisions&_json=files&_json=metadata",
            success: function (data) {
                var html = "";
                var el = data.rows[0];
                var link = "/" + db_url + "/cases/" + id;
                var decision_text = "";

                // container for case
                html+='<div class="case"';
                html += '<div class="case-text">';
                // placeholder for an eventual decision-text
                html+="<span id='decision-placeholder'></span>";
                if (el.subtitle) { html+='<div class="case-subtitle"><b>' + el.subtitle + '</b></div>'; }
                if (el.resume) { html+='<h3 class="padding-top_m">Resumé</h3><div class="case-resume">' + el.resume + '</div>'; }
                if (el.suggestion) { html+='<h3 class="padding-top_m">Indstilling</h3><div class="case-suggestion">' + el.suggestion + '</div>'; }
                if (el.presentation) { html+='<h3 class="padding-top_m">Sagsfremstilling</h3><div class="case-presentation">' + el.presentation + '</div>'; }
                if (el.notes) { html+='<h3 class="padding-top_m">Bemærkninger</h3><div class="case-notes">' + el.notes + '</div>'; }
                html += '</div>'; // .close case-text

                // decisions
                if (el.decisions) {
                    var length = el.decisions.length;
                    // html += '<div class="padding-top_l">';
                    // if (length > 1) { html+='<h3>Sagens forløb</h3><hr>'; }
                    html+='<h3 class="padding-top_l">Sagens forløb</h3><hr>';
                    // container for case-decisions
                    el.decisions.forEach( function(dict) {
                        // root-container for decision
                        html += '<div class="case-decision padding-top_m">';

                        // is this the decision from the current meeting?
                        var active_meeting = false;
                        if ((dict.meeting_id) && dict.meeting_id.toString() === current_meeting) {
                            active_meeting = true;
                        }
                        // update decision_text
                        if (active_meeting) {
                            if (dict.conclusion) {decision_text = dict.conclusion;}
                            else if (dict.title) {decision_text = dict.title;}
                            else if (dict.text) {decision_text = dict.text;}
                        }

                        // add .decision-header
                        if (dict.fora_name && length > 1) {
                            html+='<h4 class="case-decision-header margin-bottom_xs">';
                            if (dict.meeting_id && !(active_meeting)) {
                                html += '<a class="underline" href="/' + db_url + '/meetings/' + dict.meeting_id + '#' + id + '">' + localize(dict.date) + ' ' + dict.fora_name + '</a>';
                            } else if (active_meeting) {
                                html += localize(dict.date) + ' ' + dict.fora_name + '&nbsp;(dette møde)';
                            } else {
                                html += localize(dict.date) + ' ' + dict.fora_name;
                            }
                            html +='</h4>'; // close .decision-header
                        }

                        // container for decision-texts
                        html += '<div class="case-decision-texts">';
                        if (dict.conclusion) { html+= '<p class="case-decision-conclusion padding-bottom_s">' + dict.conclusion + '</p>'; }
                        if (dict.title) { html += '<p class="case-decision-title padding-bottom_s">' + dict.title + '</p>'; }
                        if (dict.text) { html += '<p class="case-decision-text padding-bottom_s">' + dict.text + '</p>'; }
                        html+='</div>'; // closing .case-decision-text

                        // container for decision-files
                        if (dict.files) {
                            html+='<div class="case-decision-files padding-left_s padding-top_s">';
                            html+='<h5>Bilag</h5>';
                            if (dict.attachment_intro) { html+='<p>' + dict.attachment_intro + ':</p>'; }
                            var sorted_files = dict.files.sort(compareValues('filename'));
                            sorted_files.forEach( function(attachment) {
                            // dict.files.forEach( function(attachment) {
                                html+='<p class="case-decision-file"><a href="' + attachment.href + '" target="_blank">' +  attachment.filename.charAt(0).toUpperCase() + attachment.filename.slice(1) + '</a></p>';
                            });
                            html += '</div>'; // closing .case-decision-files
                        }
                        html += '</div>';// closing .case-decision
                    });
                    html += '</div>'; // closing .case-decisions
                }

                // files
                if (el.files) {
                    html+='<h3 class="case-files padding-top_l">Bilag</h3>';
                    // use if wanting to sort by filename
                    //var sorted_files = el.files.sort(compareValues('filename'));
                    // sorted_files.forEach( function(attachment) {
                    el.files.forEach( function(attachment) {
                        html+='<div class="case-file"><a href="' + attachment.href + '" target="_blank">' + attachment.filename.charAt(0).toUpperCase() + attachment.filename.slice(1) + '</a></div>';
                    });
                }
                // html+='</div>'; // closing .expanded-inner

                // if decision-text is updated and the element is a record, insert the text in the placeholder
                if (decision_text && el.type === "record") {
                    // console.log(decision_text);
                    html = html.replace("<span id='decision-placeholder'></span>", "<div class='case-decision-current padding_s margin-bottom_m background_lightergray'><p class='margin-bottom_xs'><b>Beslutning (på dette møde)</b></p><p>" + decision_text + "</p></div>");
                }
                // append case to html
                $('[data-case-id="'+id+'"] + .expanded').append(html);
            }
        });
    }

    // ON PAGELOAD
    if (window.location.hash && $("body").hasClass("agenda")) {
        scroll(0, 0);
        // setTimeout(scroll(0, 0), 1); // void some browsers issue
        var anchorLink = $(window.location.hash);
        var offsetSize = $("#navigation").innerHeight() + 5;
        $("html, body").delay(400).animate({scrollTop: anchorLink.offset().top - offsetSize}, 700);
        anchorLink.focus();
    }

    // Listen for "Enter". If pressed while search-reslut in focus, trigger click (below) of .search-result
    // document.addEventListener("keyup", (e) => {
    //     if (e.keyCode == 13) {
    //         var el = document.activeElement;
    //         var parent = el.parentElement;

    //         if ( parent.querySelector(".list-group-item > .search-result") ) {
    //             el.querySelector(".search-result").click();
    //         } else if ( parent.querySelector(".list-group-item > .search-result-link") ) {
    //             el.querySelector(".search-result-link").click();
    //         } else if ( parent.querySelector(".case-link-share > .case-link-trigger") ) {
    //             el.click(); // trigger click on .case-link-anchor
    //         }
    //     }
    // });

    document.addEventListener("keyup", function(e) {
        if (e.key === "Enter") {
            var el = document.activeElement;
            var parent = el.parentElement;

            if ( parent.querySelector(".list-group-item > .search-result") ) {
                el.querySelector(".search-result").click();
            } else if ( parent.querySelector(".list-group-item > .search-result-link") ) {
                el.querySelector(".search-result-link").click();
            } else if ( parent.querySelector(".case-link-share > .case-link-trigger") ) {
                el.click(); // trigger click on .case-link-anchor
            }
        }
    });

    $(".list-group-item").each(function(e) {
        if ($(this).prev(".list-group-item").length > 0) {
            $(this).addClass("border-top_1-lightgray");
        }
    });

    $('#meetings-form, #cases-form').submit( function(e) {
        $(this).find("#inputsortdate").each( function() {
            var $cur = $(this);
            var opt_name = $cur.children("option:selected").data("name");
            $cur.prop("name", opt_name);
        });
        // console.log($(this).serialize());
        return true;
    });

    $('#search-form').submit( function(e) {
        // e.preventDefault();
        $(this).find(":input").filter(function(){ return !this.value; }).prop("name", "");

        $(this).find(":input").each( function() {
            var $cur = $(this);
            if ($cur.prop("name") === "_search") {
                if ( $("#title_only").prop("checked") ) {
                    $cur.prop("name", "_search_title");
                }
            }
        });
        return true;
    });

    // Do stuff when a case is clicked.
    $(".search-result").click(function(){

        if ($(this).data("case-id")) {
            var $this = $(this);
            var $listitem = $this.parent();
            var $hiddenSection = $listitem.find(".expanded");

            if($listitem.hasClass("is-open")) {
                $listitem.removeClass("is-open");
                $listitem.attr("aria-expanded", "false")
                $this.find(".fa-minus").removeClass("fa-minus").addClass("fa-plus");
                $hiddenSection.hide();
            }
            else {
                if ($("body").hasClass("agenda")) {
                    if (! $listitem.hasClass("item-fetched")) {
                        fetchAgendaItem($this.data("case-id"));
                        $listitem.addClass("item-fetched");
                    }
                }
                $(".list-group-item.is-open").not($listitem).find(".expanded").hide();
                $(".list-group-item.is-open").not($listitem).find(".fa-minus").removeClass("fa-minus").addClass("fa-plus");
                $listitem.addClass("is-open");
                $listitem.attr("aria-expanded", "true")
                $this.find(".fa-plus").removeClass("fa-plus").addClass("fa-minus");
                $hiddenSection.show();
                $("html, body").delay(300).animate({scrollTop: $listitem.offset().top - 100}, 500);
            }
        }
    });

    // Show/hide share link box.
    $(".case-link-share").click(function(){
        $(this).siblings(".case-link").toggleClass("is-visible");
    });

    // Mark and copy content of link.
    $(".case-link").on( "click", ".btn", function (event) {
        // $(".expanded").on( "click", ".btn", function (event) {
        if(event.handled !== true) {
            var range = document.createRange();
            range.selectNode($(this).parent().parent().find(".copy-text")[0]);
            window.getSelection().removeAllRanges(); // clear current selection
            window.getSelection().addRange(range); // to select text
            document.execCommand("copy");
            event.handled = true;
        }
    });
});
