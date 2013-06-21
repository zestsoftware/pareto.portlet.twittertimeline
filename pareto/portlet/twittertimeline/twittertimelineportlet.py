from Acquisition import aq_inner

from pareto.portlet.twittertimeline import TTMF as _

from plone.app.portlets.portlets import base
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget

from plone.portlets.interfaces import IPortletDataProvider

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

class ChromeVocabulary(object):
    """Vocabulary factory for chrome. """
    implements(IVocabularyFactory)

    def __call__(self, context):        
        items = [
            "noheader", "nofooter", "noborders", "noscrollbar","transparent"]
        items = [SimpleTerm(i, i, i) for i in items]
        return SimpleVocabulary(items)

ChromeVocabularyFactory = ChromeVocabulary()



class ITwitterTimelinePortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet. Only shows when "
            u"emulate portlet is enabled."),
        required=True)
 
    username = schema.TextLine(
        title=_(u"Username"),
        description=_(u"Create a timeline widget on https://twitter.com"
                      u"/settings/widgets/ (logged in with your account). "
                      u"Fill in the username, used for the creation of the "
                      u"Twitter Widget."),
        required=True)
  
    timeline_id = schema.TextLine(
        title=_(u"Timeline ID"),
        description=_(u"Fill in the data-timeline-id from the embed code of "
                      u"the Twitter Widget you have created for the username."
                      ),
        required=True)
  
    info = schema.Text(
        title=_(u"Information"),
        description=_(u"Short rich text area. Shows above the tweets."),
        required=False)
  
    theme = schema.Choice(
        title=_(u"Theme"),
        description=_(u""),
        values=("light", "dark"),
        required=False,
        default="light") 
  
    link_color = schema.TextLine(
        title=_(u"Link color"),
        description=_(u"Note that some icons in the timeline will also "
                      u"appear this color."),
        required=False)
  
    width = schema.TextLine(
        title=_(u"Width"),
        description=_(u"The standard HTML width attribute on the "
                      u"embed code (units are pixels.)"),
        required=False)
  
    height = schema.TextLine(
        title=_(u"Height"),
        description=_(u"The standard HTML height attribute on the "
                      u"embed code (units are pixels.)"),
        required=False)
  
    chrome = schema.List(
        title=_(u"Chrome"),
        description=_(u"Control the timeline layout and chrome. "
            u"You can use a set of the following options: "
            u" "
            u"noheader: Hides the timeline header. Please refer to the "
            u"timeline display requirements when implementing your own header."
            u" "
            u"nofooter: Hides the timeline footer and Tweet box, if included."
            u" "
            u"noborders: Removes all borders within the timeline (between "
            u"Tweets, cards, around the timeline.) See also: border-color."
            u" "
            u"noscrollbar: Crops and hides the main timeline scrollbar, if "
            u"visible. Please consider that hiding standard user interface "
            u"components can affect the accessibility of your website."
            u" "
            u"transparent: Removes the background color."),
        value_type=schema.Choice(
            source='pareto.portlet.twittertimeline.Chrome'),
        required=False,
        default=[])
  
    border_color = schema.TextLine(
        title=_(u"Border color"),
        description=_(u"Change the border color used by the timeline. Takes "
                      u"an #abc123 hex format color e.g. #cc0000"),
        required=False)
  
    lang = schema.TextLine(
        title=_(u"Language"),
        description=_(u"The timeline language is detected from the page, "
            u"based on the HTML lang attribute of your content. You can also "
            u"set the HTML lang attribute on the embed code itself."),
        required=False)
  
    tweet_limit = schema.TextLine(
        title=_(u"Tweet limit"),
        description=_(u"To fix the size of a timeline to a preset number of "
            u"Tweets, set the tweet-limit with any number between 1 and 20 "
            u"Tweets. The timeline will render the specified number of Tweets "
            u"from the timeline, expanding the height of the timeline to "
            u"display all Tweets without scrolling. Since the timeline is "
            u"of a fixed size, it will not poll for updates when using this "
            u"option."),
        required=False)
  
    related = schema.TextLine(
        title=_(u"Web Intent Related Users"),
        description=_(u"As per the Tweet and follow buttons, you may "
            u"provide a comma-separated list of user screen names as "
            u"suggested followers to a user after they reply, Retweet, or "
            u"favorite a Tweet in the timeline."),
        required=False)
  
    aria_polite = schema.Bool(
        title=_(u"ARIA politeness"),
        description=_(u"ARIA is an accessibility system that aids people "
            u"using assistive technology interacting with dynamic web "
            u"content. Read more about ARIA on W3C's website. If enabled, the "
            u"embedded timeline uses the least obtrusive setting. If using an "
            u"embedded timeline as a primary source of content on your page, "
            u"you may wish to override this to the assertive setting."),
        required=False,
        default=True)
  
    emulate_portlet = schema.Bool(
        title=_(u"Emulate portlet"),
        description=_(u"If enabled, the timeline is set as unobtrusive as "
            u"possible and rendered in a portlet instead of the standard "
            u"Twitter timeline."),
        required=False,
        default=False)

    footer = schema.TextLine(
        title=_(u"Portlet footer"),
        description=_(u"Text to be shown in the footer"),
        required=False)

    more_url = schema.ASCIILine(
        title=_(u"Details link"),
        description=_(u"If given, the header and footer "
            "will link to this URL."),
        required=False)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ITwitterTimelinePortlet)

    header = u""
    info = u""
    username = u""
    timeline_id = u""
    theme = u""
    link_color = u""
    width = u""
    height = u""
    chrome = []
    border_color = u""
    lang = u""
    tweet_limit = u""
    related = u""
    aria_polite = True
    emulate_portlet = False
    footer = u""
    more_url = ''

    def __init__(self, header = u"", info = u"", username = u"", 
        timeline_id = u"", theme = u"", link_color = u"", width = u"", 
        height = u"", chrome = [], border_color = u"", lang = u"", 
        tweet_limit = u"", related = u"", aria_polite = True, 
        emulate_portlet = False, footer = u"", more_url = ''):

        self.header = header
        self.info = info
        self.username = username
        self.timeline_id = timeline_id
        self.theme = theme
        self.link_color = link_color
        self.width = width 
        self.height = height
        self.chrome = chrome
        self.border_color = border_color
        self.lang = lang
        self.tweet_limit = tweet_limit
        self.related = related
        self.aria_polite = aria_polite
        self.emulate_portlet = emulate_portlet
        self.footer = footer
        self.more_url = more_url
     
    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Twitter Timeline: %s" % self.header


class Renderer(base.Renderer):
    """Portlet renderer. """

    render = ViewPageTemplateFile('twittertimelineportlet.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def has_link(self):
        return bool(self.data.more_url)

    def has_footer(self):
        return bool(self.data.footer)

    def init_js(self):
        return ('!function(d,s,id){'
                'var js,fjs=d.getElementsByTagName(s)[0],'
                "p=/^http:/.test(d.location)?'http':'https';"
                'if(!d.getElementById(id)){js=d.createElement(s);'
                'js.id=id;js.src=p+"://platform.twitter.com/widgets.js";'
                'fjs.parentNode.insertBefore(js,fjs);'
                '}}(document,"script","twitter-wjs");')

    def transformed(self, mt='text/x-html-safe'):
        """Use the safe_html transform to protect text output. This also
        ensures that resolve UID links are transformed into real links.
        """
        orig = self.data.info
        context = aq_inner(self.context)
        if not orig:
            return None
        if not isinstance(orig, unicode):
            # Apply a potentially lossy transformation, and hope we stored
            # utf-8 text. There were bugs in earlier versions of this portlet
            # which stored text directly as sent by the browser, which could
            # be any encoding in the world.
            orig = unicode(orig, 'utf-8', 'ignore')
            logger.warn("Static portlet at %s has stored non-unicode text. "
                "Assuming utf-8 encoding." % context.absolute_url())

        # Portal transforms needs encoded strings
        orig = orig.encode('utf-8')

        transformer = getToolByName(context, 'portal_transforms')
        data = transformer.convertTo(mt, orig,
                                     context=context, mimetype='text/html')
        result = data.getData()
        if result:
            if isinstance(result, str):
                return unicode(result, 'utf-8')
            return result
        return None


class AddForm(base.AddForm):
    """Portlet add form. """
    form_fields = form.Fields(ITwitterTimelinePortlet)
    form_fields['info'].custom_widget = WYSIWYGWidget

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form. """
    form_fields = form.Fields(ITwitterTimelinePortlet)
    form_fields['info'].custom_widget = WYSIWYGWidget
