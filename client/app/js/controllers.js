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

function UserController($scope){
    $scope.showSiteHeader(false);
    var id='4c636f6f79d1e21e62cbd815';
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


function PlaceController($scope, $routeParams,placeService) {
    $scope.$watch('coordinates', function(newValue, oldValue) {
        if (angular.isDefined($scope.coordinates)){
            var params = {
                longitude: $scope.coordinates.longitude,
                latitude: $scope.coordinates.latitude,
                placeId: $routeParams.placeId
            }
            var newsfeed = placeService.$newsfeed(
                params,
                function(){
                    $scope.distance = newsfeed.distance;
                    $scope.feed = newsfeed.messages;
                    $scope.place = newsfeed.place;
                    $scope.map = true
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

function PlaceMapController($scope, $routeParams,placeService){
    $scope.$watch('coordinates', function(newValue, oldValue) {
        if (angular.isDefined($scope.coordinates)){
            var params = {
                longitude: $scope.coordinates.longitude,
                latitude: $scope.coordinates.latitude,
                placeId: $routeParams.placeId
            }
            var newsfeed = placeService.$newsfeed(
                params,
                function(){
                    $scope.place = newsfeed.place;
                    $scope.placeHeader = newsfeed.place;
                    $scope.distance = newsfeed.distance;
                    $scope.map = true
                    $scope.myMarker = true;
                });
        }
    });
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
                    $scope.feedPhoto=feed.messages;
                    $scope.placeHeader = feed.place
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
            $scope.placeHeader = message.place
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
    $scope.autoCompleteList = [
    {'name':'балетки','category':'shoes'},{'name':'бахилы','category':'shoes'},{'name':'башмак','category':'shoes'},{'name':'берцы','category':'shoes'},{'name':'болотники','category':'shoes'},{'name':'босоножки','category':'shoes'},{'name':'ботильоны','category':'shoes'},{'name':'ботинки','category':'shoes'},{'name':'ботинки','category':'shoes'},{'name':'ботфорты','category':'shoes'},{'name':'боты','category':'shoes'},{'name':'броги','category':'shoes'},{'name':'бродни','category':'shoes'},{'name':'бурки','category':'shoes'},{'name':'бутсы','category':'shoes'},{'name':'валенки','category':'shoes'},{'name':'вьетнамки','category':'shoes'},{'name':'галоши','category':'shoes'},{'name':'гриндерс','category':'shoes'},{'name':'гэта','category':'shoes'},{'name':'дезерты','category':'shoes'},{'name':'дерби','category':'shoes'},{'name':'джазовки','category':'shoes'},{'name':'доктор мартинс','category':'shoes'},{'name':'калоши','category':'shoes'},{'name':'кеды','category':'shoes'},{'name':'конверс','category':'shoes'},
{'name':'кроссовки','category':'shoes'},{'name':'лодочки','category':'shoes'},{'name':'лоферы','category':'shoes'},{'name':'мартинсы','category':'shoes'},{'name':'мокасины','category':'shoes'},{'name':'монки','category':'shoes'},{'name':'мюли','category':'shoes'},{'name':'оксфорды','category':'shoes'},{'name':'пимы','category':'shoes'},{'name':'пинетки','category':'shoes'},{'name':'полуботинки','category':'shoes'},{'name':'полукеды','category':'shoes'},{'name':'пуанты','category':'shoes'},{'name':'сабо','category':'shoes'},{'name':'сандалии','category':'shoes'},{'name':'сапоги','category':'shoes'},{'name':'сланцы','category':'shoes'},{'name':'слипоны','category':'shoes'},{'name':'сникерсы','category':'shoes'},{'name':'таби','category':'shoes'},{'name':'тапки','category':'shoes'},{'name':'трикони','category':'shoes'},{'name':'туфли','category':'shoes'},{'name':'тэйлорс','category':'shoes'},{'name':'угги','category':'shoes'},{'name':'унты','category':'shoes'},{'name':'унты','category':'shoes'},{'name':'шлепанцы','category':'shoes'},{'name':'шлепки','category':'shoes'},{'name':'штиблеты','category':'shoes'},
    {'name':'бабочка','category':'accessories'},{'name':'бижутерия','category':'accessories'},{'name':'боа','category':'accessories'},{'name':'браслеты','category':'accessories'},{'name':'брелок','category':'accessories'},{'name':'варежки','category':'accessories'},{'name':'галстук','category':'accessories'},{'name':'горжетка','category':'accessories'},{'name':'зонт','category':'accessories'},{'name':'камербанд','category':'accessories'},{'name':'кашне','category':'accessories'},{'name':'ключница','category':'accessories'},{'name':'кошелек','category':'accessories'},{'name':'краги','category':'accessories'},{'name':'маска','category':'accessories'},{'name':'митенки','category':'accessories'},{'name':'монокль','category':'accessories'},{'name':'муфта','category':'accessories'},{'name':'шарф','category':'accessories'},{'name':'напульсник','category':'accessories'},{'name':'оби','category':'accessories'},{'name':'очки','category':'accessories'},{'name':'палстрон','category':'accessories'},{'name':'перчатки','category':'accessories'},{'name':'платок','category':'accessories'},{'name':'подтяжки','category':'accessories'},{'name':'портупея','category':'accessories'},{'name':'варежки','category':'accessories'},{'name':'пояс','category':'accessories'},{'name':'ремень','category':'accessories'},{'name':'руковицы','category':'accessories'},{'name':'рэйбан','category':'accessories'},{'name':'рэйбэн','category':'accessories'},{'name':'стельки','category':'accessories'},{'name':'торк','category':'accessories'},{'name':'торквес','category':'accessories'},{'name':'фенечки','category':'accessories'},{'name':'четки','category':'accessories'},{'name':'шаль','category':'accessories'},{'name':'шнурки','category':'accessories'},
    {'name':'бикини','category':'under'},{'name':'боди','category':'under'},{'name':'бойшортс','category':'under'},{'name':'боксеры','category':'under'},{'name':'брифы','category':'under'},{'name':'бюстглалтер','category':'under'},{'name':'бюстье','category':'under'},{'name':'виктория сикретс','category':'under'},{'name':'комбинация','category':'under'},{'name':'корсаж','category':'under'},{'name':'корсет','category':'under'},{'name':'купальник','category':'under'},{'name':'кюлот','category':'under'},{'name':'лифчик','category':'under'},{'name':'панталоны','category':'under'},{'name':'пенюар','category':'under'},{'name':'пижама','category':'under'},{'name':'плавки','category':'under'},{'name':'подвязки','category':'under'},{'name':'семейники','category':'under'},{'name':'слипы','category':'under'},{'name':'стринги','category':'under'},{'name':'танга','category':'under'},{'name':'термобелье','category':'under'},{'name':'тонг','category':'under'},{'name':'трусы','category':'under'},{'name':'халат','category':'under'},{'name':'чайки','category':'under'},
    {'name':'бермуды','category':'trousers'},{'name':'бриджи','category':'trousers'},{'name':'брюки','category':'trousers'},{'name':'бэгги','category':'trousers'},{'name':'джегенсы','category':'trousers'},{'name':'джинсы','category':'trousers'},{'name':'капри','category':'trousers'},{'name':'карго','category':'trousers'},{'name':'леггинсы','category':'trousers'},{'name':'ледерхозе','category':'trousers'},{'name':'лосины','category':'trousers'},{'name':'скинни','category':'trousers'},{'name':'хакама','category':'trousers'},{'name':'шаровары','category':'trousers'},{'name':'шорты','category':'trousers'},{'name':'штаны','category':'trousers'},
    {'name':'альстер','category':'outer'},{'name':'анорак','category':'outer'},{'name':'балмаакан','category':'outer'},{'name':'берберри','category':'outer'},{'name':'бомбер','category':'outer'},{'name':'бострог','category':'outer'},{'name':'бурнус','category':'outer'},{'name':'бушлат','category':'outer'},{'name':'ватник','category':'outer'},{'name':'ветровка','category':'outer'},{'name':'дафлкот','category':'outer'},{'name':'дождевик','category':'outer'},{'name':'дубленка','category':'outer'},{'name':'зипун','category':'outer'},{'name':'инвернес','category':'outer'},{'name':'коверт','category':'outer'},{'name':'колет','category':'outer'},{'name':'косуха','category':'outer'},{'name':'котарди','category':'outer'},{'name':'куртка','category':'outer'},{'name':'макинтош','category':'outer'},{'name':'ментик','category':'outer'},{'name':'пальто','category':'outer'},{'name':'парка','category':'outer'},{'name':'пехора','category':'outer'},{'name':'пихора','category':'outer'},{'name':'плащ','category':'outer'},{'name':'плащ-палатка','category':'outer'},{'name':'полупальто','category':'outer'},{'name':'полушубок','category':'outer'},{'name':'пончо','category':'outer'},{'name':'пуховик','category':'outer'},{'name':'телогрейка','category':'outer'},{'name':'тренч','category':'outer'},{'name':'тренчкот','category':'outer'},{'name':'тужурка','category':'outer'},{'name':'тулуп','category':'outer'},{'name':'хавелок','category':'outer'},{'name':'чапан','category':'outer'},{'name':'честерфилд','category':'outer'},{'name':'шинель','category':'outer'},{'name':'штормовик','category':'outer'},{'name':'шуба','category':'outer'},
    {'name':'акубра','category':'head'},{'name':'афганка','category':'head'},{'name':'балаклава','category':'head'},{'name':'балморал','category':'head'},{'name':'бандана','category':'head'},{'name':'бейсболка','category':'head'},{'name':'берет','category':'head'},{'name':'бескозырка','category':'head'},{'name':'боливар','category':'head'},{'name':'борсалино','category':'head'},{'name':'буденовка','category':'head'},{'name':'венок','category':'head'},{'name':'вуаль','category':'head'},{'name':'галеро','category':'head'},{'name':'гренадерка','category':'head'},{'name':'дастар','category':'head'},{'name':'двууголка','category':'head'},{'name':'диадема','category':'head'},{'name':'ермолка','category':'head'},{'name':'канотье','category':'head'},{'name':'капор','category':'head'},{'name':'каса','category':'head'},{'name':'каска','category':'head'},{'name':'кепи','category':'head'},{'name':'кепка','category':'head'},{'name':'кипа','category':'head'},{'name':'клош','category':'head'},{'name':'колпак','category':'head'},{'name':'конфидератка','category':'head'},{'name':'коппола','category':'head'},{'name':'корона','category':'head'},{'name':'косынка','category':'head'},{'name':'котелок','category':'head'},{'name':'куфия','category':'head'},{'name':'мантилья','category':'head'},{'name':'наушники','category':'head'},{'name':'панама','category':'head'},{'name':'папаха','category':'head'},{'name':'пилотка','category':'head'},{'name':'платок','category':'head'},{'name':'плюмаж','category':'head'},{'name':'повязка','category':'head'},{'name':'сомбреро','category':'head'},{'name':'треуголка','category':'head'},{'name':'трилби','category':'head'},{'name':'тэм-о-шентер','category':'head'},{'name':'тюбитейка','category':'head'},{'name':'тюрбан','category':'head'},{'name':'ушанка','category':'head'},{'name':'феска','category':'head'},{'name':'фуражка','category':'head'},{'name':'хиджаб','category':'head'},{'name':'хомбург','category':'head'},{'name':'цилиндр','category':'head'},{'name':'чепец','category':'head'},{'name':'шапка','category':'head'},{'name':'шапокляк','category':'head'},{'name':'шлем','category':'head'},
    {'name':'болеро','category':'top2'},{'name':'джемпер','category':'top2'},{'name':'жакет','category':'top2'},{'name':'жилет','category':'top2'},{'name':'камзол','category':'top2'},{'name':'кардиган','category':'top2'},{'name':'кофта','category':'top2'},{'name':'лопапейса','category':'top2'},{'name':'накидка','category':'top2'},{'name':'палантин','category':'top2'},{'name':'пиджак','category':'top2'},{'name':'пуловер','category':'top2'},{'name':'свитер','category':'top2'},{'name':'смокинг','category':'top2'},{'name':'сюртук','category':'top2'},{'name':'фрак','category':'top2'},{'name':'френч','category':'top2'},{'name':'худи','category':'top2'},
    {'name':'кейгори','category':'suits'},{'name':'кимоно','category':'suits'},{'name':'комбинизон','category':'suits'},{'name':'костюм','category':'suits'},{'name':'кэтсьют','category':'suits'},{'name':'платье','category':'suits'},{'name':'сарафан','category':'suits'},{'name':'сари','category':'suits'},{'name':'тоги','category':'suits'},{'name':'тройка','category':'suits'},{'name':'туника','category':'suits'},{'name':'фурсьют','category':'suits'},
    {'name':'авоська','category':'bags'},{'name':'баул','category':'bags'},{'name':'борсетка','category':'bags'},{'name':'дипломат','category':'bags'},{'name':'клатч','category':'bags'},{'name':'кофр','category':'bags'},{'name':'несессер','category':'bags'},{'name':'подсумок','category':'bags'},{'name':'портфель','category':'bags'},{'name':'ранец','category':'bags'},{'name':'ридикюль','category':'bags'},{'name':'рюкзак','category':'bags'},{'name':'саквояж','category':'bags'},{'name':'сумка','category':'bags'},{'name':'фуросики','category':'bags'},{'name':'футляр','category':'bags'},{'name':'чемодан','category':'bags'},
    {'name':'алкоголичка','category':'top1'},{'name':'бадлон','category':'top1'},{'name':'банлон','category':'top1'},{'name':'безрукавка','category':'top1'},{'name':'блузка','category':'top1'},{'name':'бодлон','category':'top1'},{'name':'водолазка','category':'top1'},{'name':'гимнастерка','category':'top1'},{'name':'косоворотка','category':'top1'},{'name':'лонгслив','category':'top1'},{'name':'майка','category':'top1'},{'name':'поло','category':'top1'},{'name':'рубашка','category':'top1'},{'name':'седре','category':'top1'},{'name':'сорочка','category':'top1'},{'name':'спагетти','category':'top1'},{'name':'тельняшка','category':'top1'},{'name':'толстовка','category':'top1'},{'name':'топ','category':'top1'},{'name':'тэнниска','category':'top1'},{'name':'фланелевка','category':'top1'},{'name':'футболка','category':'top1'},{'name':'фуфайка','category':'top1'},
    {'name':'гетры','category':'socks'},{'name':'гольфы','category':'socks'},{'name':'колготки','category':'socks'},{'name':'колготы','category':'socks'},{'name':'носки','category':'socks'},{'name':'портянки','category':'socks'},{'name':'рейтузы','category':'socks'},{'name':'термобелье','category':'socks'},
    {'name':'чулки','category':'skirts'},{'name':'американка','category':'skirts'},{'name':'годе','category':'skirts'},{'name':'карандаш','category':'skirts'},{'name':'килт','category':'skirts'},{'name':'колокол','category':'skirts'},{'name':'кринолин','category':'skirts'},{'name':'мини','category':'skirts'},{'name':'парео','category':'skirts'},{'name':'пачка','category':'skirts'},{'name':'полусолнце','category':'skirts'},{'name':'саронг','category':'skirts'},{'name':'солнце','category':'skirts'},{'name':'тюлбпан','category':'skirts'},{'name':'юбка','category':'skirts'}
    ]
    $scope.showSiteHeader(false);
    $scope.filter = {query:'',radius:0};
    $scope.showSearchResults = false;
    $scope.isSearch = false;
    
    $scope.showAutoComplete = function(){
        if($scope.showSearchResults){return false}
        else{return $scope.filter.query}
    }
    $scope.$watch('showSearchResults',function(){
        if(!$scope.showSearchResults){$scope.changeScrollToDown()}
        else{$scope.changeScrollToUp()}
    })

    var newList = function(){
        $scope.isSearch = true;
        var params = {}
        if($scope.filter.radius){params.radius=$scope.filter.radius}
        if($scope.filter.query){params.query=$scope.filter.query}
        $location.path('/search').search(params)
        if (angular.isDefined($scope.coordinates)){
            params.latitude = $scope.coordinates.latitude,
            params.longitude = $scope.coordinates.longitude
            $scope.searchFeed = messageService.search(params,
                                                      function(){
                                                          $scope.isSearch = false;
                                                          $scope.showSearchResults = true;
                                                    })
        }
    }
    
    var getSearchPlaceList = function(){
        $scope.isSearch = true;
        var params = {}
        params.query = $scope.filter.query
        if($scope.filter.radius){params.radius = $scope.filter.radius}
        if (angular.isDefined($scope.coordinates)){
            params.latitude = $scope.coordinates.latitude,
            params.longitude = $scope.coordinates.longitude
            $scope.searchPlaceList=placeService.search(
                params,
                function(){
                    $scope.isSearch = false;
                }
            );
        }
    }
    
    $scope.$on(events.searchFilter.changed, function(name, filter){
        var query = filter.query;
        var radius = filter.radius;
        if(query && query==$scope.filter.query){
            if(radius==$scope.filter.radius){
                $scope.filter = filter;
            }
            else{
                $scope.filter = filter;
                newList()
            }
        }
        else{
            $scope.filter = filter;
            $scope.searchFeed = []
            $scope.showSearchResults = false;
            getSearchPlaceList()
        }
    });
    
    $scope.newQuery = function(query){
        if(query){
            $scope.filter.query = query;
            newList()
        }
    }
    
    
    
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
    var initialize = function(){
        if($routeParams.query!=$scope.query){$scope.query = $routeParams.query || null;}
        if($routeParams.radius!=$scope.radius){$scope.radius = $routeParams.radius || 0;}
    }
    initialize();
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
            if (newValue.length > 2 || newValue == ''){
                if (refresh != null)
                    $timeout.cancel(refresh);
                refresh = $timeout(onChangedHandler, 1000)
            }
        }
    });

    $scope.$watch('radius', function(newValue, oldValue){
        if (newValue != oldValue)
            onChangedHandler();
    });
    
    if($scope.query){onChangedHandler();}
    
    $scope.$on('$routeUpdate', function(){
        initialize();
    });
}

function MessageEditorController($location, $scope, $routeParams, placeService, messagePreviewService) {
    if (angular.isDefined($routeParams.placeId))
        placeService.get({placeId: $routeParams.placeId}, function(resp){ $scope.placeHeader = resp; })
    if (angular.isDefined($routeParams.previewId))
        messagePreviewService.get({previewId: $routeParams.previewId}, function(response){
            $scope.text = response.text;
            $scope.photoUrl = response.photo.thumbnail;
            $scope.place = response.place;
        });
    $scope.inProgress = false;
    $scope.showPhoto = true;
 
    $scope.removePhoto = function(){
        $scope.photo = null;
//         $scope.showPhoto = false;
    }
    $scope.send = function() {
        $scope.inProgress = true;
        var message = new FormData();
        
        message.append( 'place', $routeParams.placeId);
        message.append( 'text', $scope.text);
//         if($scope.photo){
            message.append( 'photo', $scope.photo);
//         }
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
            $scope.placeHeader = preview.place;
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
    $scope.showSiteHeader(false);
    $scope.isSearch = false;
    $scope.filter = { radius: 0, query: ''};
    $scope.$on(events.searchFilter.changed, function(name, filter){
        $scope.filter = filter
        refresh()
    })
    var refresh = function(){
        $scope.isSearch = true;
        var params = {}
        if (angular.isDefined($scope.coordinates)){
            if($scope.filter.query){params.query=$scope.filter.query}
            if($scope.filter.radius){params.radius=$scope.filter.radius}
            params.latitude = $scope.coordinates.latitude;
            params.longitude = $scope.coordinates.longitude;
            placeService.searchInVenues(
                params,
                function(options){ $scope.options = options; $scope.isSearch = false;}
            );
        }
    };
    $scope.$watch('coordinates', refresh());
//     $scope.$watch('filter.radius', $scope.refresh);
//     var refresh = null;
//     $scope.$watch('filter.query', function(newValue, oldValue){
//         if (newValue != oldValue && (newValue.length > 3 || newValue == '')){
//             if (refresh != null)
//                 $timeout.cancel(refresh);
//             refresh = $timeout($scope.refresh, 2000)
//         }
//     });
    $scope.clearFilter = function(){
        $scope.filter = { radius: 0, query: ''};
    }
}