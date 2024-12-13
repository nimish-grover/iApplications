from flask import url_for


class HelperClass():
    def get_supply_menu():
        return [
            { "route" : url_for('.status'), "label":"back", "icon":"fa-solid fa-left-long"},
            { "route" : url_for('.surface'), "label":"surface", "icon":"fa-solid fa-water"},
            { "route" : url_for('.ground'), "label":"ground", "icon":"fa-solid fa-arrow-up-from-ground-water"},
            { "route" : url_for('.lulc'), "label":"lulc", "icon":"fa-solid fa-cloud-showers-water"},
            { "route" : url_for('.rainfall'), "label":"rainfall", "icon":"fa-solid fa-cloud-rain"},
        ]

    def get_demand_menu():
        return [
            { "route" : url_for('.status'), "label":"back", "icon":"fa-solid fa-left-long"},
            { "route" : url_for('.human'), "label":"human", "icon":"fa-solid fa-people-roof"},
            { "route" : url_for('.livestocks'), "label":"livestock", "icon":"fa-solid fa-paw"},
            { "route" : url_for('.crops'), "label":"crops", "icon":"fa-brands fa-pagelines"},
            { "route" : url_for('.industries'), "label":"industries", "icon":"fa-solid fa-industry"},
        ]
    
    def get_main_menu():
        return [
            { "route" : url_for('mobile.index'), "label":"index", "icon":"fa-solid fa-house"},
            { "route" : url_for('desktop.human'), "label":"demand", "icon":"fa-solid fa-chart-line"},
            { "route" : url_for('desktop.surface'), "label":"supply", "icon":"fa-solid fa-glass-water-droplet"},
            { "route" : url_for('desktop.status'), "label":"status", "icon":"fa-solid fa-list-check"},
            { "route" : url_for('desktop.transfer'), "label":"transfer", "icon":"fa-solid fa-arrow-right-arrow-left"},
        ]
    
    def get_breadcrumbs(payload):
        """
        Generate breadcrumb navigation based on the current payload.

        Returns:
            list: Breadcrumbs for the current context.
        """
        return [
            {'name': payload['state_name'], 'href': '#'},
            {'name': payload['district_name'], 'href': '#'},
            {'name': payload['block_name'], 'href': '#'}
        ]