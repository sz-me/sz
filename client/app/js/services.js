'use strict';

/* Services */

angular.module('sz.client.services', ['ngResource'])
	.factory('Places', function($resource){
		return $resource('../api/places.txt', {}, {
			query: { method:'GET', params:{}, isArray:false } 
		});
	});