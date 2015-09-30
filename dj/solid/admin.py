from django.contrib import admin

from mezzanine.core.admin import TabularDynamicInlineAdmin, StackedDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin

import mezzanine.core.admin as aaa

from solid.models import Portfolio, PortfolioItem, PortfolioItemCategory, PortfolioItemImage, PortfolioSkill,\
    PortfolioSkillUsed


class PortfolioItemImageInline(TabularDynamicInlineAdmin):
    model = PortfolioItemImage


class PortfolioSkillUsedInline(TabularDynamicInlineAdmin):
    model = PortfolioSkillUsed


class PortfolioItemAdmin(PageAdmin):
    exclude = ('skills',)
    inlines = (PortfolioItemImageInline, PortfolioSkillUsedInline)


admin.site.register(Portfolio, PageAdmin)
admin.site.register(PortfolioItem, PortfolioItemAdmin)

# These are just models, not full page admins.
admin.site.register(PortfolioItemCategory)
admin.site.register(PortfolioSkill)
