$(function(){
    if (navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(function(data) {

            var latitude = data.coords.latitude;
            var longitude = data.coords.longitude;
            var page = new sz.light.models.PageModel();
            page.set('position', { longitude: longitude, latitude: latitude });



            var LightRouter = Backbone.Router.extend({
                routes: {
                    "": "feed",
                    "!/": "feed",
                    "!/q/:query/:subject/:distance": "feed",
                    "!/v/:id": "place",
                    "!/403": "forbidden"
                },

                feed: function (query, subject, distance) {
                    page.set('state', sz.light.models.pageStates.Feed)
                    if (query)
                        page.models[sz.light.models.pageStates.Feed].set('query', query);
                    if (subject)
                        page.models[sz.light.models.pageStates.Feed].set('subject', subject);
                    if (distance)
                        page.models[sz.light.models.pageStates.Feed].set('distance', distance);
                    page.models[sz.light.models.pageStates.Feed].refreshPlaces();
                },

                place: function () {
                    page.set('state', sz.light.models.pageStates.Place)
                },

                forbidden:
                    function(){
                        alert(403);
                    }

            });

            var router = new LightRouter();

            var pageView = new sz.light.views.PageView({
                model: page,
                el: $("#page"),
                router: router
            });
            var username = $("#username").val();
            page.set('user', username);

            Backbone.history.start();  // Запускаем HTML5 History push
        });





    }
    else
        $("#page").html("Geolocation services are not supported by your browser " +
            "or you do not have a GPS device in your computer.");
});

