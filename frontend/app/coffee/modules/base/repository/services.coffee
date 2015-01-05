kquotes = @kquotes


class RepositoryService extends kquotes.Service
    @.$inject = ["$q", "$kqModel", "$kqStorage", "$kqHttp", "$kqUrls"]

    constructor: (@q, @model, @storage, @http, @urls) ->
        super()

    resolveUrlForModel: (model) ->
        idAttrName = model.getIdAttrName()
        return "#{@urls.resolve(model.getName())}/#{model[idAttrName]}"

    resolveUrlForAttributeModel: (model) ->
        return @urls.resolve(model.getName(), model.parent)

    create: (name, data, dataTypes={}, extraParams={}) ->
        defered = @q.defer()
        url = @urls.resolve(name)

        promise = @http.post(url, JSON.stringify(data))
        promise.success (_data, _status) =>
            defered.resolve(@model.make_model(name, _data, null, dataTypes))

        promise.error (data, status) =>
            defered.reject(data)

        return defered.promise

    remove: (model, params={}) ->
        defered = @q.defer()
        url = @.resolveUrlForModel(model)

        promise = @http.delete(url, {}, params)
        promise.success (data, status) ->
            defered.resolve(model)

        promise.error (data, status) ->
            defered.reject(model)

        return defered.promise

    saveAll: (models, patch=true) ->
        promises = _.map(models, (x) => @.save(x, true))
        return @q.all(promises)

    save: (model, patch=true) ->
        defered = @q.defer()

        if not model.isModified() and patch
            defered.resolve(model)
            return defered.promise

        url = @.resolveUrlForModel(model)
        data = JSON.stringify(model.getAttrs(patch))

        if patch
            promise = @http.patch(url, data)
        else
            promise = @http.put(url, data)

        promise.success (data, status) =>
            model._isModified = false
            model._attrs = _.extend(model.getAttrs(), data)
            model._modifiedAttrs = {}

            model.applyCasts()
            defered.resolve(model)

        promise.error (data, status) ->
            defered.reject(data)

        return defered.promise

    saveAttribute: (model, attribute, patch=true) ->
        defered = @q.defer()

        if not model.isModified() and patch
            defered.resolve(model)
            return defered.promise

        url = @.resolveUrlForAttributeModel(model)

        data = {}

        data[attribute] = model.getAttrs()

        if patch
            promise = @http.patch(url, data)
        else
            promise = @http.put(url, data)

        promise.success (data, status) =>
            model._isModified = false
            model._attrs = _.extend(model.getAttrs(), data)
            model._modifiedAttrs = {}

            model.applyCasts()
            defered.resolve(model)

        promise.error (data, status) ->
            defered.reject(data)

        return defered.promise

    refresh: (model) ->
        defered = @q.defer()

        url = @.resolveUrlForModel(model)
        promise = @http.get(url)
        promise.success (data, status) ->
            model._modifiedAttrs = {}
            model._attrs = data
            model._isModified = false
            model.applyCasts()
            defered.resolve(model)

        promise.error (data, status) ->
            defered.reject(data)

        return defered.promise

    queryMany: (name, params, options={}) ->
        url = @urls.resolve(name)
        httpOptions = {headers: {}}

        if not options.enablePagination
            httpOptions.headers["x-disable-pagination"] =  "1"

        return @http.get(url, params, httpOptions).then (data) =>
            return _.map(data.data, (x) => @model.make_model(name, x))

    queryOneAttribute: (name, id, attribute, params, options={}) ->
        url = @urls.resolve(name, id)
        httpOptions = {headers: {}}

        if not options.enablePagination
            httpOptions.headers["x-disable-pagination"] =  "1"

        return @http.get(url, params, httpOptions).then (data) =>
            model = @model.make_model(name, data.data[attribute])
            model.parent = id

            return model

    queryOne: (name, id, params, options={}) ->
        url = @urls.resolve(name)
        url = "#{url}/#{id}" if id
        httpOptions = {headers: {}}
        if not options.enablePagination
            httpOptions.headers["x-disable-pagination"] =  "1"

        return @http.get(url, params, httpOptions).then (data) =>
            return @model.make_model(name, data.data)

    queryOneRaw: (name, id, params, options={}) ->
        url = @urls.resolve(name)
        url = "#{url}/#{id}" if id
        httpOptions = _.merge({headers: {}}, options)
        if not options.enablePagination
            httpOptions.headers["x-disable-pagination"] =  "1"
        return @http.get(url, params, httpOptions).then (data) =>
            return data.data

    queryPaginated: (name, params, options={}) ->
        url = @urls.resolve(name)
        httpOptions = _.merge({headers: {}}, options)
        return @http.get(url, params, httpOptions).then (data) =>
            headers = data.headers()
            result = {}
            result.models = _.map(data.data, (x) => @model.make_model(name, x))
            result.count = parseInt(headers["x-pagination-count"], 10)
            result.current = parseInt(headers["x-pagination-current"] or 1, 10)
            result.paginatedBy = parseInt(headers["x-paginated-by"], 10)
            return result


module = angular.module("kquotesBase")
module.service("$kqRepo", RepositoryService)