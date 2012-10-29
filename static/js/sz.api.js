var sz = {};
sz.Api = function(options){
    this.uri = options.uri;
    this.format = options.format;
    this.request_func = options.request_func
    this.request = function(verb, resource, parameters, success){
        this.request_func({
            url: this.uri + resource,
            contentType: this.format = options.format,
            type: verb,
            data: parameters,
            success: success
            }
        );
    };
    this.get = function(resource, parameters, success) { return this.request('GET', resource, parameters, success); };
    this.post = function(resource, parameters, success) { return this.request('POST', resource, parameters, success); };
}