var sz = sz || {};
sz.light = sz.light || {};
sz.light.views = sz.light.views || {};

sz.light.views.PageView = Backbone.View.extend({
    views: {},
    initialize: function () {
        this.router = this.options.router;
        this.template = _.template($('#regularPageTemplate').html());
        this.model.on('change:user', this.render, this);
        this.views[sz.light.models.pageStates.Feed] = sz.light.views.FeedView;
    },
    render: function () {
        this.$el.html(this.template(this.model));
        var state = this.model.get("state");
        var view = new this.views[state]({
            el: $("#content"),
            model: this.model.models[state],
            router: this.router,
            page: this
        });
        this.model.on('change:position', view.changePosition, this);
        view.render();
        return this;
    }
});

sz.light.views.LoadingView = Backbone.View.extend({
    views: {
        loading: {}},
    initialize: function () {
        this.template = _.template($('#loadingTemplate').html());
    },
    render: function () {
        this.$el.html(this.template(this.model));
        return this;
    }
});

sz.light.views.FeedView = Backbone.View.extend({
    views: {
        loading: {}},
    initialize: function () {
        this.router = this.options.router;
        this.page = this.options.page;
        this.template = _.template($('#feedTemplate').html());
    },
    render: function () {
        this.$el.html(this.template(this.model));
        this.filterView = new sz.light.views.FilterView({
            el: $('#filter'),
            model: this.model,
            router: this.router
        });
        this.filterView.render();
        var places = this.model.get('places');
        this.placesView = new sz.light.views.PlacesView({
            el: $('#places'),
            model: places,
            router: this.router
        });
        places.on('reset', this.placesView.render, this.placesView);
        return this;
    },
    changePosition: function(){
        // Todo: refresh PlacesView
    }
});

sz.light.views.FilterView = Backbone.View.extend({
    initialize: function () {
        this.router = this.options.router;
        this.template = _.template($('#filterTemplate').html());
    },
    events: {
        "submit form": "submitForm"
    },
    render: function () {
        this.$el.html(this.template(this.model));
        return this;
    },

    submitForm: function(){
        var query = this.$el.find("input[name=searchQuery]").val();
        var subject = this.$el.find("input[name='searchSubject']:checked").val();
        var nearby = this.$el.find("input[name='searchDistance']").is(":checked");
        this.model.set('query', query);
        this.model.set('subject', subject);
        if (nearby)
            this.model.set('distance', sz.light.models.SearchDistance.Nearby);
        else
            this.model.set('distance', sz.light.models.SearchDistance.Anywhere);
        this.router.navigate(this.model.getFragment(), {trigger: true});
        return false;
    }
});

sz.light.views.PlacesView = Backbone.View.extend({
    initialize: function () {
        this.router = this.options.router;
        this.template = _.template($('#placeListItemTemplate').html());
    },
    events: {

    },
    render: function () {
        var itemHtml = this.template;
        var html = _(this.model.models).reduce(function(acc, place){ return acc + itemHtml(place.toJSON()); }, '');
        this.$el.html(html);
        return this;
    }

});