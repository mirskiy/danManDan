from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _     # TODO do we want translation? prolly not

from mezzanine.pages.models import Page
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.core.fields import FileField, RichTextField
from mezzanine.utils.models import upload_to


# from django.db import models
#
#
# class Project(models.Model):
#     name = models.CharField(max_length=100)     # TODO google cuts after 56, minus 9 for danmandan. WARN if > 45
#     slug = models.SlugField(max_length=25, unique=True)
#     description = models.TextField()
#     date_started = models.DateField()
#     date_completed = models.DateField(null=True, blank=True)
#
#     def __str__(self):
#         return self.name


# ----- PORTFOLIO STUFF -----
class PortfolioSkill(Slugged):
    """ A skill, such as Python or HW. Each Portfolio item can link to skills with a through model """
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Portfolio Skill")
        verbose_name_plural = _("Portfolio Skills")
        ordering = ("title",)


class PortfolioSkillUsed(models.Model):
    """ Through model to relate items to skills with description and rating """
    skill = models.ForeignKey('PortfolioSkill')
    item = models.ForeignKey('PortfolioItem', related_name="skillsused")
    description = models.CharField(max_length=100, help_text="The way this skill was used.")
    rating = models.IntegerField(help_text="How heavily the skill was used on a scale of 1-10, 10=A lot.",
                                 validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        ordering = ('-rating',)


class Portfolio(Page):
    """ A collection of individual portfolio items """
    content = RichTextField(blank=True)

    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")


class PortfolioItem(Page, RichText):
    """
    An individual portfolio item, should be nested under a Portfolio
    """
    # TODO
    # Need to have location, time period, position!
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=25)
    location = models.CharField(max_length=25)
    featured_image = FileField(
        verbose_name=_("Featured Image"),
        upload_to=upload_to("solid.PortfolioItem.featured_image", "portfolio"),
        format="Image", max_length=255, null=True, blank=True)
    # TODO short description should be at most 3 lines (of whaat width lol?)
    # add a validator and ask chris
    short_description = RichTextField(blank=True,
                                      help_text="Should be at most 3 lines! Check to make sure it isn't cut off")
    categories = models.ManyToManyField("PortfolioItemCategory",
                                        verbose_name=_("Categories"),
                                        blank=True,
                                        related_name="portfolioitems")
    skills = models.ManyToManyField('PortfolioSkill',
                                    through=PortfolioSkillUsed,
                                    verbose_name=_("Skills"),
                                    blank=True,
                                    related_name="portfolioitems")
    href = models.CharField(max_length=2000, blank=True,
                            help_text="A link to the finished project (optional)")

    def _date_range(self):
        """ Represents start_date to end_date nicely """
        date_format = "%b '%y"
        start_date_str = self.start_date.strftime(date_format)

        if self.end_date is None:
            return start_date_str + "- Now"

        end_date_str = self.end_date.strftime(date_format)

        if start_date_str == end_date_str:
            return start_date_str

        return start_date_str + " - " + end_date_str
    date_range = property(_date_range)

    class Meta:
        verbose_name = _("Portfolio item")
        verbose_name_plural = _("Portfolio items")


class PortfolioItemImage(Orderable):
    """
    An image for a PortfolioItem
    """
    portfolioitem = models.ForeignKey(PortfolioItem, related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
        upload_to=upload_to("solid.PortfolioItemImage.file", "portfolio items"))

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class PortfolioItemCategory(Slugged):
    """
    A category for grouping portfolio items into a series.
    """

    class Meta:
        verbose_name = _("Portfolio Item Category")
        verbose_name_plural = _("Portfolio Item Categories")
        # ordering = ("title",)     # TODO inherit from oderable?
