def format_proposal_title(document):
    if document.document_type and document.year and document.number:
        proposal_title = "%s %s/%s" % (document.document_type.initials,
                                       document.year, document.number)
    else:
        proposal_title = document.title

    return proposal_title
