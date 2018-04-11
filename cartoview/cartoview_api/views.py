from django.shortcuts import render, HttpResponse
from geonode.layers.views import layer_detail
import json
# Create your views here.


# TODO: check if function is provided by geonode
def layer_config_json(request, layername):
    layer_details = layer_detail(
        request, layername)
    viewer = layer_details.context_data['viewer']
    layer = layer_details.context_data['resource']
    # TODO: check Projection
    viewer = json.loads(viewer)
    # Todo: check if srid is not settled
    layer.set_bounds_from_bbox(layer.bbox[0:4], layer.srid)
    center = [layer.center_x, layer.center_y]
    zoom = layer.zoom
    viewer['map']['center'] = center
    viewer['map']['zoom'] = zoom
    return HttpResponse(json.dumps(viewer), content_type="application/json")
