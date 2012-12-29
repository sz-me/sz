var sz = sz || {};
sz.light = {};
sz.light.static = {};

sz.light.ControlView = function(){
    this.textId = 'query_' + new Date().valueOf();
    this.nearbyCheckboxId = "nearby_" + new Date().valueOf();
    this.messageRadioId = "message_" + new Date().valueOf();
    this.placeRadioId = "place_" + new Date().valueOf();
    this.searchMenuContainerId = "search-menu_" + new Date().valueOf();
    this.postingMenuContainerId = "posting-menu_" + new Date().valueOf();
    this.cancelButtonId = 'cancel-button_' + new Date().valueOf();
    this.submitButtonId = 'submit-button_' + new Date().valueOf();
    this.getHtmlSearchMenu = function(model){
        return '<menu id="' + this.searchMenuContainerId + '">' +
            '<label for = "' + this.messageRadioId + '">things</label>' +
            '<input type = "radio"' +
            'name = "sz_lite_what"' +
            'id = "' + this.messageRadioId + '"' +
            'value = "message"' +
            'checked = "checked"' +
            'class = "message-radio" />' +
            ' or ' +
            '<label for = "' + this.placeRadioId + '">places</label>' +
            '<input type = "radio"' +
            'name = "sz_lite_what"' +
            'id = "' + this.placeRadioId + '"' +
            'value = "place"' +
            'class = "place-radio" />' +
            '<label for="' + this.nearbyCheckboxId + '">nearby</label>' +
            '<input id="' + this.nearbyCheckboxId + '" type="checkbox" title="nearby"/>' +
            '</menu>';
    };
    this.getHtmlPostingMenu = function(model){
        return '<menu id="' + this.postingMenuContainerId + '" hidden>' +
            '<button class="submit-button" id="' + this.submitButtonId + '">Post</button>' +
            '<button class="cancel-button" id="' + this.cancelButtonId + '">Back</button>' +
            '</menu>';
    };
    this.getHtml = function(model){
        return  '<label for="'+ this.textId +'">Search</label> ' +
                '<input type="search" id="' + this.textId + '" class="input-search-text" />' +
                this.getHtmlSearchMenu(model) +
                this.getHtmlPostingMenu(model)
            ;
    };
    this.showSearch = function(){
        $('label[for="' + this.textId + '"]').text('Search');
        $('#' + this.postingMenuContainerId).hide();
        $('#' + this.searchMenuContainerId).show();
    };
    this.showPosting = function(){
        $('label[for="' + this.textId + '"]').text('Post');
        $('#' + this.searchMenuContainerId).hide();
        $('#' + this.postingMenuContainerId).show();
    };
    this.getText = function(){
        return $('#' + this.textId).val();
    }
    this.getSearchParams = function(){
        var nearby = $('#' + this.nearbyCheckboxId).is(':checked');
        var isMessage = $('#' + this.messageRadioId).is(':checked');
        var query = this.getText();
        var params = {}
        if (isMessage)
            params.message = query;
        else
            params.place = query;
        if (nearby)
            params.nearby = '';
        return params;
    };
};

sz.light.viewMessages = function(messages){
    var html = '<ul>';
    $.each(messages, function(i, message) {
        html += '<li> <time>' + new Date(message.date).toDateString() + '</time> ' +
            message.text + ' ~@' + message.username +
            '</li>'
    });
    html += '</ul>';
    return html;
}
sz.light.viewCategories = function(categories){
    var html = '<ul class="place-summary">';
    $.each(categories, function(i, category) {
        html += '<code>#' + category.name + '(' + category.count + ')' + '</code> '
    });
    html += '</ul>';
    return html;
}
sz.light.FeedView = function(){
    this.messageAdditionButtonCssClass = 'message-addition-button';
    function viewFeed(model, messageAdditionButtonCssClass){
            var html = '';
            html += '<ul>';
            $.each(model, function(i, place){
                html += '<li id="' + place.url + '"' + '>' +
                    '<button type="button" ' +
                    'class="' + messageAdditionButtonCssClass + '"' +
                    'value="' + place.url + '"' + '>+' +
                    place.name + '</button> ' ;
                if (place.address != null)
                    html += place.address + ', ';
                dist = Math.floor(place.distance);
                html += dist + 'm';
                html += (sz.light.viewCategories(place.categories))
                html += sz.light.viewMessages(place.messages.results);

                html += '</li>';
            });
            html += '</ul>';
            return html;
    }
    this.getHtml = function(model){
        return viewFeed(model, this.messageAdditionButtonCssClass);
    };
};

sz.light.DetailsView = function(){
    this.getHtml = function(model){
        messages = sz.light.viewMessages(model.messages.results);
        var html = '<h1>' + model.name + ', ' + Math.floor(model.distance) + 'm</h1>';

        if (model.address != null && model.crossStreet != null)
            html += '<p>' + model.address + ' (' + model.crossStreet + ')' + '</p>';
        else
        {
            if (model.address != null)
                html += '<p>' + model.address + '</p>';
            if (model.crossStreet != null)
                html += '<p>' + model.crossStreet + '</p>';
        }

        if (model.contact != '{}')
            html += '<p>' + model.contact + '</p>';
        html += '<p><a href="' + model.foursquare_details_url +'">' + model.foursquare_details_url + '</a></p>'
        html += sz.light.viewCategories(model.categories)
        html += messages;

        return html;



    };
};

sz.light.LoadingView = function(){
    this.control = null;
    this.getHtml = function(model){
        if (model == null)
            return 'Loading...';
        else return model;
    };
};

sz.light.static.map = null;
sz.light.static.marker = null;
sz.light.showMap = function(model){
    var myLatlng = new google.maps.LatLng(model.position[1], model.position[0]);
    var myOptions = {
        zoom: 16,
        center: myLatlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    if ($("#map_canvas").is(':hidden'))
    {
        $("#map_canvas").show();

        if (sz.light.static.map == null)
            sz.light.static.map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
        else
            sz.light.static.map.setCenter(myLatlng)

        if (sz.light.static.marker == null)
            sz.light.static.marker = new google.maps.Marker({
                position: myLatlng,
                map: sz.light.static.map,
                title: model.name
            });
        else
            sz.light.static.marker.setPosition(myLatlng);
            sz.light.static.marker.setZIndex(google.maps.Marker.MAX_ZINDEX + 1);
    }
}

sz.light.static.controllers = {};
sz.light.static.controllers.responseHandler = function(controller, response, success, forbidden, error){
    if (response.meta.code == 403){
        if (forbidden == null){
            if (controller.forbiddenHandler != null )
                controller.forbiddenHandler();
            else
                document.location = '/api-auth/login/?next=/light/';
        }
        else
            forbidden(controller, response.data || response.meta)
    }
    else if(response.meta.code == 200 || response.meta.code == 201)
        success(controller, response.data);
    else{
        if (error == null)
            alert(response.meta.code);
        else
            error(controller, response.data || response.meta)
    }
}

sz.light.Controller = function(api, feedContainer, controlContainer){

    this.defaultUrl = '/api/places/';
    this.currentUrl = this.defaultUrl;
    this.currentAction = null;
    this.api = api;
    this.position = null;

    //actions
    this.action = function(action, url, params, verb, success, forbidden, error){
        this.currentAction = action;
        var p = params();
        p.longitude = this.position.longitude;
        p.latitude = this.position.latitude;
        var controller = this;
        verb.call(this.api, url, p,
            function(response){
                sz.light.static.controllers.responseHandler(controller, response, success, forbidden, error);
            });
    };

    this.loadingAction = function(message){
        this.containers.feed.html(this.views.loading.getHtml(message));
    };

    this.detailsAction = function(){
        this.loadingAction(null);
        var controller = this;
        var success = function(controller, model){
            controller.views.control.showPosting();
            sz.light.showMap(model);
            var html = controller.views.details.getHtml(model);
            controller.containers.feed.html(html);
        }
        var params = function(){
            var text = controller.views.control.getText.call(controller.views.control);
            if (text != null)
                if (!(!text.length || /^\s*$/.test(text)))
                    return {message: text};
            return {};
        };
        this.action(this.detailsAction, this.currentUrl,
            params, this.api.get, success, null, null);
    };
    this.feedAction = function(){
        $('#map_canvas').hide()
        this.loadingAction(null);
        var controller = this;
        controller.currentUrl = controller.defaultUrl;
        var success = function(controller, model){
            controller.views.control.showSearch();
            var html = controller.views.feed.getHtml(model);
            controller.containers.feed.html(html);
            $("." + controller.views.feed.messageAdditionButtonCssClass)
                .click({controller: controller}, function(e){
                    e.data.controller.currentUrl = $(this).val();
                    e.data.controller.detailsAction();
                });

        }
        var params = function(){
            return controller.views.control.getSearchParams.call(controller.views.control);
        };
        this.action(this.feedAction, this.currentUrl,
            params, this.api.get, success, null, null);
    };
    this.postAction = function(){
        var controller = this;
        var success = function(controller, model){
            var text = model.things.join(', ');
            $('#' + controller.views.control.messageRadioId).attr('checked', true);
            controller.oldControlText = text;
            $('#' + controller.views.control.textId).val(text);
            controller.feedAction();
        }
        var params = function(){
            var text = controller.views.control.getText.call(controller.views.control);
            if (text != null)
                if (!(!text.length || /^\s*$/.test(text)))
                    return {
                        text: text,
                        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                    };
            return {};
        };
        this.action(controller.detailsAction, controller.currentUrl + 'messages/',
            params, controller.api.post, success, null, null);
    };

    this.views = {};
    this.views.feed = new sz.light.FeedView();
    this.views.details = new sz.light.DetailsView();
    this.views.loading = new sz.light.LoadingView();
    this.views.control = new sz.light.ControlView();

    this.containers = {
        feed: feedContainer,
        control: controlContainer
    };

    this.loadingAction('Position location...');
    var controlHtml = this.views.control.getHtml(null);
    controlContainer.html(controlHtml);
    this.oldControlText = this.views.control.getText();

    this.forbiddenHandler = null;

    // events
    $('#' + this.views.control.submitButtonId).click(
        {controller: this},
        function(e) {
            e.data.controller.postAction();
        });
    $('#' + this.views.control.cancelButtonId).click(
        {controller: this},
        function(e) {
            e.data.controller.feedAction();
        });

    $('#' + this.views.control.messageRadioId).change({controller: this}, function(e){
        if (e.data.controller.currentAction != null) e.data.controller.currentAction(); });
    $('#' + this.views.control.placeRadioId).change({controller: this}, function(e){
        if (e.data.controller.currentAction != null) e.data.controller.currentAction(); });
    $('#' + this.views.control.nearbyCheckboxId).change({controller: this}, function(e){
        if (e.data.controller.currentAction != null) e.data.controller.currentAction(); });

    this.detectControlTextChange = function (controller){
        var text = controller.views.control.getText();
        if (controller.oldControlText != text){
            if (controller.currentAction != null) controller.currentAction();
            controller.oldControlText = text;
        }
    };
};