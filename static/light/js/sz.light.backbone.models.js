var sz = sz || {};
sz.light = sz.light || {};
sz.light.models = sz.light.models || {};

sz.light.views = sz.light.models.pageStates ={
    Feed: 'feed',
    Place: 'place'
}

sz.light.models.PageModel = Backbone.Model.extend({
    defaults: function() {
        return {
            state: sz.light.models.pageStates.Feed,
            position: null,
            user: null,
            models: { }
        };
    },
    initialize: function() {
        this.models = {};
        this.models[sz.light.models.pageStates.Feed] = new sz.light.models.FeedModel({page: this});
        this.on('change:position', this.changePosition, this);
    },
    changePosition: function() {
        var position = this.get("position");
        if (position != null)
            this.set('state', 'feed');
    }
});

sz.light.models.SearchSubject = {
        Things : 'thing',
        Places : 'place'
    }
sz.light.models.SearchDistance = {
        Anywhere : 'anywhere',
        Nearby : 'nearby'
    }

sz.light.models.FeedModel = Backbone.Model.extend({
    defaults: function() {
        return {
            page: null,
            query: '',
            subject: sz.light.models.SearchSubject.Things,
            distance: sz.light.models.SearchDistance.Anywhere,
            places: new sz.light.models.PlaceCollection()
        };
    },
    initialize: function() {
    },
    getFragment: function(){
        return "!/q/" + this.get("query") + '/' + this.get("subject") + '/' + this.get("distance");
    },
    refreshPlaces: function(){
        page = this.get('page');
        position = page.get('position');
        var params = {};
        params.latitude = position.latitude;
        params.longitude = position.longitude;
        if (this.get('subject') == sz.light.models.SearchSubject.Places)
            params.place = this.get('query');
        else
            params.message = this.get('query');
        var places = this.get('places');
        places.fetch({data: params});
    }
});

sz.light.models.PlaceModel = Backbone.Model.extend({
});
sz.light.models.PlaceCollection = Backbone.Collection.extend({
    model: sz.light.models.PlaceModel,
    url: '../../api/places/',
    parse: function(response) {
        return response.data;
    }
});
