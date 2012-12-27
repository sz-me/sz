var sz = sz || {};
sz.light = {};
sz.light.views = {};

sz.light.ControlView = function(){
    this.textId = 'query_' + new Date().valueOf();
    this.nearbyCheckboxId = "nearby_" + new Date().valueOf();
    this.messageRadioId = "message_" + new Date().valueOf();
    this.placeRadioId = "place_" + new Date().valueOf();
    this.searchMenuContainerId = "search-menu_" + new Date().valueOf();
    this.postingMenuContainerId = "posting-menu_" + new Date().valueOf();
    this.cancelButtonCssClass = 'cancel-button';
    this.submitButtonCssClass = 'submit-button';
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
            '<button class="submit-button">Post</button>' +
            '<button class="cancel-button">Back</button>' +
            '</menu>';
    };
    this.getHtml = function(model){
        return  '<label for="'+ this.textId +'">Search</label>' +
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

sz.light.FeedView = function(){
    this.messageAdditionButtonCssClass = 'message-addition-button';
    function viewMessages(messages){
        var html = '<ul>';
        $.each(messages, function(i, message) {
            html += '<li> <em>' + new Date(message.date).toDateString() + '</em> ' + message.text + '</li>'
        });
        html += '</ul>';
        return html;
    }
    function viewCategories(categories){
        var html = '<ul class="place-summary">';
        $.each(categories, function(i, category) {
            html += '<code>#' + category.name + '(' + category.count + ')' + '</code> '
        });
        html += '</ul>';
        return html;
    }
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
                html += (viewCategories(place.categories))
                html += viewMessages(place.messages.results);

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
        return 'Details';
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

sz.light.Controller = function(api, feedContainer, controlContainer){
    this.api = api;
    this.position = null;

    this.views = {};
    this.views.feed = new sz.light.FeedView();
    this.views.details = new sz.light.DetailsView();
    this.views.loading = new sz.light.LoadingView();
    this.views.control = new sz.light.ControlView();

    this.containers = {
        feed: feedContainer,
        control: controlContainer
    };
    this.loadingAction = function(message){
        this.containers.feed.html(this.views.loading.getHtml(message));
    };
    this.loadingAction('Position location...');
    var controlHtml = this.views.control.getHtml(null);
    controlContainer.html(controlHtml);
    this.oldControlText = this.views.control.getText();

    this.error403Handler = null;

    this.detailsAction = function(url, params){
        this.loadingAction(null);
        this.views.control.showPosting();
        var html = this.views.details.getHtml(null);
        this.containers.feed.html(html);
    };
    this.feedAction = function(){
        this.loadingAction(null);
        var params = this.views.control.getSearchParams();
        params.longitude = this.position.longitude;
        params.latitude = this.position.latitude;
        var controller = this;
        this.api.get('/api/places/',
            params,
            function(response){
                if (response.meta.code == 403){
                    if (controller.error403Handler != null )
                        controller.error403Handler();
                    else
                        document.location = '/api-auth/login/?next=/light/'
                }
                else if(response.meta.code == 200)
                {
                    controller.views.control.showSearch();
                    var html = controller.views.feed.getHtml(response.data);
                    controller.containers.feed.html(html);
                    $("." + controller.views.feed.messageAdditionButtonCssClass)
                        .click({controller: controller}, function(e){
                            e.data.controller.detailsAction($(this).val(), null);
                        });
                }
                else
                    alert(response.meta.code);
            });

    };




    // events
    $('.' + this.views.control.cancelButtonCssClass).click(
        {controller: this},
        function(e) {
            e.data.controller.feedAction();
        });

    $('#' + this.views.control.messageRadioId).change({controller: this}, function(e){
        e.data.controller.feedAction(); });
    $('#' + this.views.control.placeRadioId).change({controller: this}, function(e){
        e.data.controller.feedAction(); });
    $('#' + this.views.control.nearbyCheckboxId).change({controller: this}, function(e){
        e.data.controller.feedAction(); });

    this.detectControlTextChange = function (controller){
        var text = controller.views.control.getText();
        if (controller.oldControlText != text){
            controller.feedAction();
            controller.oldControlText = text;
        }
    };
};