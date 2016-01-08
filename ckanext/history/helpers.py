import ckan.model as model
import ckan.plugins.toolkit as toolkit

from ckan.common import c


def dataset_revisions(pkg_name, pkg_revisions):
    """
    :param pkg_name: name or id of package
    :type pkg_name: str
    :param pkg_revisions: revision details
    :type pkg_revisions: list of dicts

    :return: string
    """

    context = {'model': model, 'session': model.Session, 'user': c.user}

    revisions_dict = {}

    revision_order = []
    for revision in pkg_revisions:

        # The revision id needs to be passed through the context rather than data_dict (base CKAN quirk)
        context['revision_id'] = revision['id']

        revision_pkg = toolkit.get_action('package_show')(context, {'id': pkg_name})
        revisions_dict[revision['id']] = revision_pkg

        revision_order.append(revision['id'])

    def _pairs(lst):
        i = iter(lst)
        prev = i.next()
        for item in i:
            yield prev, item
            prev = item

    revisions_to_compare = _pairs(revision_order)

    next_record = {}
    modified_fields_dict = {}

    for pair in revisions_to_compare:

        new_dict = revisions_dict[pair[0]]
        old_dict = revisions_dict[pair[1]]

        modified_fields_dict[pair[0]] = []
        for k, v in new_dict.iteritems():

            try:
                if old_dict[k] != new_dict[k]:
                    modified_fields_dict[pair[0]].append(k)
            except KeyError:
                modified_fields_dict[pair[0]].append(k)  # also include added and deleted fields

        modified_fields_dict[pair[0]].sort()

        next_record[pair[0]] = pair[1]

    return {'modified_fields': modified_fields_dict, 'next_record': next_record}
