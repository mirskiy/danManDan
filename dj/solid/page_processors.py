from mezzanine.pages.page_processors import processor_for
from .models import Portfolio, PortfolioItem, PortfolioItemCategory, PortfolioSkill


@processor_for(Portfolio)
def portfolio_processor(request, page):
    """Add a portfolio's portfolio items to the context"""
    # get the Portfolio's items, prefetching categories for performance
    items = PortfolioItem.objects.published(for_user=request.user).prefetch_related('categories')
    items = items.filter(parent=page)

    # skills = PortfolioSkill.objects.filter(portfolioitems__in=items).distinct()
    skills = PortfolioSkill.objects.all()

    # filter out only categories that are used in the Portfolio's items
    categories = PortfolioItemCategory.objects.filter(portfolioitems__in=items).distinct()
    # TODO later prolly make categories ordered and just loop over all of them, making the section title = title
    relevant_work_category = PortfolioItemCategory.objects.get(title="Relevant work")        # Is this the best way?
    return {'portfolio_items': items, 'skills': skills, 'categories': categories,
            "relevant_work_category": relevant_work_category}
