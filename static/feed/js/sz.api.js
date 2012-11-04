var sz = {};
sz.Api = function(options){
    this.uri = options.uri;
    this.request_func = options.request_func
    this.request = function(verb, resource, parameters, response_handler){
        var resource_uri = resource;
        if (resource_uri.indexOf('http://') == -1 && resource_uri.indexOf('https://') == -1)
            resource_uri = this.uri + resource_uri;
        parameters.format = 'json';

        this.request_func(
        {
            url: resource_uri,
            contentType: 'JSON',
            type: verb,
            data: parameters,
            success: response_handler,
            error: function(jqXHR, textStatus, errorThrown) { response_handler(JSON.parse(jqXHR.responseText)); }
        });
    }

    this.get = function(resource, parameters, success) { return this.request('GET', resource, parameters, success); };
    this.post = function(resource, parameters, success) { return this.request('POST', resource, parameters, success); };
    this.put = function(resource, parameters, success) { return this.request('PUT', resource, parameters, success); };
    this.del = function(resource, parameters, success) { return this.request('DELETE', resource, parameters, success); };
}