function MasterPageController($scope,$cookies, $http, $location, geolocation, categoryService, session) {

    $scope.isSiteHeaderShown = true;

    $scope.showSiteHeader = function(value){
        $scope.isSiteHeaderShown = value;
    }

    $scope.$on('$routeChangeSuccess', function(event, routeData){
        $scope.showSiteHeader(true);
    });

    $scope.isGeolocationInProgress = false;
    $scope.$watch('session.username', function(newValue, oldValue) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
    });

    session.current({}, function(session){$scope.session = session});

    geolocation.getCurrentPosition(
        function (position) { $scope.coordinates = position.coords; },
        function (error) { $scope.coordinates = { longitude: 128, latitude: 56 }; /*$location.path('/errors/geolocation');*/ }
    )

    categoryService.query({}, function(categories) { $scope.categories = categories; });

    $scope.showContent = true;
    $scope.showMenuPanel = true;
    $scope.showBotMenuPanel = true;
    $scope.scrollToTop = {top:false};

    $scope.changeScrollToUp = function(){$scope.showBotMenuPanel = true;};
    $scope.changeScrollToDown = function(){$scope.showBotMenuPanel = false;};

    $scope.isTopMenuCollapsed = true;
    $scope.toggleTopMenu = function(){
        $scope.isTopMenuCollapsed = !$scope.isTopMenuCollapsed;
    }
}

MasterPageController.$inject = ['$scope','$cookies', '$http', '$location', 'geolocationService', 'categoryService', 'sessionService'];


function LoginController($scope) {
    $scope.login = function(username, password){
        $scope.session.username = username;
        $scope.session.password = password;
        $scope.session = $scope.session.$login();
    }
}


function RegistrationController($scope){
    $scope.registration = function(){}
}


function NewsFeedController($routeParams, $location, $scope, placeService) {
    $scope.category = '';
    $scope.radiusActive = 0
    $scope.$watch('coordinates', function(newValue, oldValue) {
        if (angular.isDefined($scope.coordinates)){
            var params = {};
            if($routeParams.radius){
                params.radius = $routeParams.radius
                $scope.radiusActive = params.radius
            }
            if($routeParams.query){params.query = $routeParams.query}
            if($routeParams.category>0){
                params.category = $routeParams.category
                $.each($scope.categories,function(index,cat){
                    if(cat.id==params.category){
                        $scope.category = cat;
                    }
                })
            }
            params.longitude = $scope.coordinates.longitude;
            params.latitude = $scope.coordinates.latitude;
            $scope.feed = placeService.newsfeed(
                params
            );
        }
    });
    
    $scope.setRadius = function(radius){
        var params = {}
        if(radius){params.radius = radius};
        if($routeParams.category>0){params.category = $routeParams.category;}
        $location.path('/newsfeed').search(params)
    }
    

    $scope.$watch('category',function(){
        var params = {}
        if($scope.category){
            params.category = $scope.category.id
        }       
        if($routeParams.radius){
            params.radius = $routeParams.radius
        }
        $location.path('/newsfeed').search(params)
    })
    
    $scope.loadMorePlaces = function(){
        if ($scope.feed.params.offset + $scope.feed.params.limit < $scope.feed.count)
        {
            $scope.feed.params.offset += $scope.feed.params.limit;
            var feed = placeService.newsfeed($scope.feed.params, function() {
                    if(feed.results.length>0){
                        $.each(feed.results,function(index,r){
                            $scope.feed.results.push(r)
                        });
                        $scope.feed.params = feed.params;
                    }
                    else{$scope.$emit($scope.scrollToTop.top=true);}
                }
            );
        }
    }
    $scope.placeMessagesLimit = 1;
    $scope.showAllPlaceMessages = function(len,lim){
        if(lim==1){return len}
        else{return 1}
    }
    $scope.showAllPlaceMessagesText = function(len,lim){
        if(lim==1){return 'Еще '+len+' сообщений'}
        else{return 'Свернуть'}
    }
}


function PlaceController($scope, $routeParams, placeService) {
    $scope.$watch('coordinates', function(newValue, oldValue) {
        if (angular.isDefined($scope.coordinates)){
            var params = {
                longitude: $scope.coordinates.longitude,
                latitude: $scope.coordinates.latitude,
                placeId: $routeParams.placeId
            }
            if($routeParams.query) {params.query = $routeParams.query}
            var newsfeed = placeService.$newsfeed(
                params,
                function(){
                    $scope.distance = newsfeed.distance;
                    $scope.feed = newsfeed.messages;
                    $scope.place = newsfeed.place;
                    $scope.feedPhoto = newsfeed.photos;
                });
        }
    });


    $scope.loadMore = function(){
        var oldFeed = $scope.feed;
        if (oldFeed.params.offset + oldFeed.params.limit < oldFeed.count)
        {
            oldFeed.params.offset += oldFeed.params.limit;
            oldFeed.params['placeId'] = $routeParams.placeId;
            oldFeed.params['longitude'] = $scope.coordinates.longitude;
            oldFeed.params['latitude'] = $scope.coordinates.latitude;
            var feed = placeService.$newsfeed(oldFeed.params,
                function() {
                    if(feed.messages.results.length>0){
                        $.each(feed.messages.results,function(index,r){
                            $scope.feed.results.push(r)
                        });
                        $scope.feed.params = feed.messages.params;
                    }
                    else{$scope.$emit($scope.scrollToTop.top=true);}
                }
            );
        }
    }
}

function GalleryController($scope, $routeParams, placeService){
    $scope.$watch('coordinates', function(newValue, oldValue) {
        if (angular.isDefined($scope.coordinates))
            var feed = placeService.$newsfeed({
                    longitude: $scope.coordinates.longitude,
                    latitude: $scope.coordinates.latitude,
                    placeId: $routeParams.placeId,
                    photo: true
                },
                function(){
                    $scope.distance = feed.distance;
                    $scope.place=feed.place;
                    $scope.feedPhoto=feed.messages;
                });
    });
    $scope.loadMore = function(){
        if ($scope.feedPhoto.params.offset + $scope.feedPhoto.params.limit < $scope.feedPhoto.count)
        {
            $scope.feedPhoto.params.offset += $scope.feedPhoto.params.limit;
            $scope.feedPhoto.params['placeId'] = $routeParams.placeId;
            $scope.feedPhoto.params['longitude'] = $scope.coordinates.longitude;
            $scope.feedPhoto.params['latitude'] = $scope.coordinates.latitude;
            var feed = placeService.$newsfeed($scope.feedPhoto.params,
                function() {
                    if(feed.photos.results.length>0){
                        $.each(feed.photos.results,function(index,r){
                            $scope.feedPhoto.results.push(r)
                        })
//                         $scope.feedPhoto.params = feed.photos.params;
                    }
                    else{$scope.$emit($scope.scrollToTop.top=true);}
                }
            );
        }
    }
}

function MessageController($scope, $routeParams, messageService){
    var message = messageService.get({messageId:$routeParams.messageId},
        function(){
            $scope.message = message;
            $scope.message_categories = [];
            $.each($scope.message.categories,function(index,catID){
                $.each($scope.categories,function(index,cat){
                    if(catID==cat.id){
                        $scope.message_categories.push(cat)
                    }
                })
            });
            if($scope.message_categories[0]){$scope.photoStyle = {marginBottom:'-60px'}}
        })
}


var events = {};
events.searchFilter = {};
events.searchFilter.changed = 'searchFilterWasChanged';
events.searchFilter.typing = 'searchFilterQueryIsBeingTyped';


function SearchController($scope, $location, messageService,placeService){
    $scope.showSiteHeader(false);
    $scope.$on(events.searchFilter.changed, function(name, filter){
        $scope.filter = filter;
    });

    $scope.showSearchResults = false;
    $scope.$watch('showSearchResults',function(){
        if(!$scope.showSearchResults){
            $scope.changeScrollToDown()
        }
        else{
            $scope.changeScrollToUp()
        }
    })

    $scope.loadMore = function(){
        if ($scope.searchFeed.params.offset + $scope.searchFeed.params.limit < $scope.searchFeed.count)
        {
            $scope.searchFeed.params.offset += $scope.searchFeed.params.limit;
            var feed = messageService.search($scope.searchFeed.params, function() {
                    if(feed.results.length>0){
                        $.each(feed.results,function(index,r){
                            $scope.searchFeed.results.push(r)
                        });
                        $scope.searchFeed.params = feed.params;
                    }
                    else{$scope.$emit($scope.scrollToTop.top=true);}
                }
            );
        }
    }
}


function SearchFilterController($scope, $timeout, $routeParams){
    $scope.query = $routeParams.query || null;
    $scope.radius = $routeParams.radius || 0;
    var onChangedHandler = function(){
        $scope.$emit(events.searchFilter.changed, {query: $scope.query, radius: $scope.radius})
    }
    var onTypingHandler = function(){
        $scope.$emit(events.searchFilter.typing, {query: $scope.query, radius: $scope.radius})
    }

    var refresh = null;
    $scope.$watch('query', function(newValue, oldValue){
        if (newValue != oldValue)
        {
            onTypingHandler();
            if (newValue.length > 3 || newValue == ''){
                if (refresh != null)
                    $timeout.cancel(refresh);
                refresh = $timeout(onChangedHandler, 2000)
            }
        }
    });

    $scope.$watch('radius', function(newValue, oldValue){
        if (newValue != oldValue)
            onChangedHandler();
    });
}

function MessageEditorController($location, $scope, $routeParams, placeService, messagePreviewService) {
    if (angular.isDefined($routeParams.placeId))
        placeService.get({placeId: $routeParams.placeId}, function(resp){ $scope.place = resp; })
    if (angular.isDefined($routeParams.previewId))
        messagePreviewService.get({previewId: $routeParams.previewId}, function(response){
            $scope.text = response.text;
            $scope.photoUrl = response.photo.thumbnail;
            $scope.place = response.place;
        });
    $scope.inProgress = false;
    
    $scope.send = function() {
        $scope.inProgress = true;
        var message = new FormData();
        message.append( 'place', $routeParams.placeId);
        message.append( 'text', $scope.text);
        message.append( 'photo', $scope.photo);
        message.append( 'smile', 1);

        var redirectToPublish = function(previewId){
            var pub_page_url = '/messages/previews/' + previewId + '/publish';
            $location.path(pub_page_url);
        }

        if (angular.isUndefined($routeParams.previewId))
            messagePreviewService.create(message,
                function(response){
                    $scope.inProgress = false;
                    $scope.response = response;
                    var edit_page_url = '/messages/previews/' + $scope.response.id + '/edit';
                    //$location.replace()
                    history.replaceState(null, "SZ - Edit message", '#' + edit_page_url);
                    redirectToPublish(response.id);
                },
                function(error){alert(angular.toJson(error, true));});
        else
            messagePreviewService.update($routeParams.previewId, message,
                function(response){
                    $scope.inProgress = false;
                    $scope.response = response;
                    redirectToPublish(response.id);
                },
                function(error){alert(angular.toJson(error, true));});

    }
}


function MessagePublisherController($location, $scope, $routeParams, messagePreviewService) {
    $scope.inProgress = false;
    $scope.showPreviewTex = false;
    $scope.new_message_categories = [];
    if (angular.isDefined($routeParams.previewId))
        var preview = messagePreviewService.get({previewId: $routeParams.previewId}, function(){
            $scope.preview = preview;
            $scope.add_categories = []
            $.each($scope.categories, function(index,cat){$scope.add_categories.push(cat)});
            $.each($scope.preview.categories, function(index,catID){
                $.each($scope.categories,function(index,cat){
                    if(catID == cat.id){
                        $scope.new_message_categories.push(cat)
                    }
                });
            });            
            for (i in $scope.add_categories){
                var cat = $scope.add_categories[i];
                for (j in $scope.preview.categories){
                    var catID = $scope.preview.categories[j]
                    if(catID==cat.id){$scope.add_categories.splice(i,1)}
                }
            }                
            
        });
    
//     $scope.$watch('new_message_categories',function(){
//         $scope.previewResource.categories = []
//         $.each($scope.new_message_categories,)
//         
//     })
    
    $scope.addCat = function(){
        if($scope.add_message_category){
            $scope.new_message_categories.push($scope.add_message_category);
            for (i in $scope.add_categories){
                var cat = $scope.add_categories[i];
                if(cat.id==$scope.add_message_category.id){
                    $scope.add_categories.splice(i,1)
                }
            }
            $scope.add_message_category = ''
        }
    }
        
    $scope.removeCat = function(messageCat,index){
        $scope.new_message_categories.splice(index, 1);
        $scope.add_categories.push(messageCat)
    }
    $scope.ok = function(){
        $scope.inProgress = true;
        $scope.preview.categories = []
        $.each($scope.new_message_categories,function(index,messageCat){
            $scope.preview.categories.push(messageCat.id)
        })
        $scope.preview.$publish(
            {},
            function(){
                var path = '/places/' + $scope.preview.place.id;
                $location.path(path);
            },
            function(error){
                $scope.inProgress = false;
                throw "can't publish";
            }
        )
    }
}


function PlaceSelectionController($scope, $timeout, placeService){
    $scope.isSearch = false;
    $scope.filter = { radius: 0, query: ''};

    $scope.refresh = function(){
        $scope.isSearch = true;
        if (angular.isDefined($scope.coordinates))
            placeService.searchInVenues({
                longitude: $scope.coordinates.longitude, latitude: $scope.coordinates.latitude,
                radius: $scope.filter.radius, query: $scope.filter.query
            }, function(options){ $scope.options = options; $scope.isSearch = false;});
    };

    $scope.$watch('coordinates', $scope.refresh);
    $scope.$watch('filter.radius', $scope.refresh);
    var refresh = null;
    $scope.$watch('filter.query', function(newValue, oldValue){
        if (newValue != oldValue && (newValue.length > 3 || newValue == '')){
            if (refresh != null)
                $timeout.cancel(refresh);
            refresh = $timeout($scope.refresh, 2000)
        }
    });
    $scope.clearFilter = function(){
        $scope.filter = { radius: 0, query: ''};
    }
}