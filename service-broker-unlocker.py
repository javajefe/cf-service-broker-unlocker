import bottle
import os


@bottle.route('/v2/service_instances/<instance_id>', method='DELETE')
def deprovision(instance_id):
    return {}

@bottle.route('/v2/service_instances/<instance_id>/service_bindings/<binding_id>', method='DELETE')
def unbind(instance_id, binding_id):
    return {}

if __name__ == '__main__':
    port = int(os.getenv('PORT', '8080'))
    bottle.run(host='0.0.0.0', port=port, debug=True, reloader=False)