from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from pareto.portlet.twitterwidget import TwitterWidgetMessageFactory as _


class ITwitterWidgetPortlet(IPortletDataProvider):
    """ TwitterWidgetPortlet
        ====================

        <a class="twitter-timeline" 
           href="https://twitter.com/twitterapi" 
           data-widget-id="YOUR-WIDGET-ID-HERE" 
           data-link-color="#cc0000"  
           data-theme="dark" 
           width="300" 
           height="500" 
           data-chrome="noheader nofooter noborders noscrollbar transparent"
           data-border-color="#cc0000"
           lang="EN" 
           data-tweet-limit="3"
           data-related="twitterapi,twitter" 
           data-aria-polite="assertive">Tweets by @twitterapi</a>
 

       data-widget-id="YOUR-WIDGET-ID-HERE" 
       data-link-color="#cc0000"  
       data-theme="dark" 
       width="300" 
       height="500" 
       data-chrome="noheader nofooter noborders noscrollbar transparent"
       data-border-color="#cc0000"
       lang="EN" 
       data-tweet-limit="3"
       data-related="twitterapi,twitter" 
       data-aria-polite="polite"

"""
    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet. Only shows when "
            u"emulate portlet is enabled."),
        required=True)

    info = schema.Text(
        title=_(u"Information"),
        description=_(u"Short rich text area. Only shows when emulate portlet "
            u"is enabled."),
        required=False)

    username = schema.TextLine(
        title=_(u"Username"),
        description=_(u''),
        required=True)

    widget_id = schema.TextLine(
        title=_(u"Widget ID"),
        description=_(u''),
        required=True)

    theme = schema.Choice(
        title=_(u"Theme"),
        description=_(u'Set by adding a data-theme="dark" attribute to the '
                      u'embed code.'),
        values=("light", "dark"),
        required=True,
        default="light") 

    link_color = schema.TextLine(
        title=_(u"Link color"),
        description=_(u'Set by adding a data-link-color="#cc0000" attribute. '
            u'Note that some icons in the widget will also appear this color.'
            ),
        required=False)

    width = schema.Int(
        title=_(u"Width"),
        description=_(u'Set using the standard HTML width attribute on the '
            u'embed code (units are pixels.)'),
        required=False)

    height = schema.Int(
        title=_(u"Height"),
        description=_(u'Set using the standard HTML height attribute on the '
            u'embed code (units are pixels.)'),
        required=True)

    chrome = schema.Choice(
        title=_(u"Chrome"),
        description=_(u'Control the widget layout and chrome by using the '
            u'data-chrome="nofooter transparent" attribute on the embed code. '
            u'Use a space-separated set of the following options: '
            u''
            u'noheader: Hides the timeline header. Please refer to the '
            u'timeline display requirements when implementing your own header.'
            u''
            u'nofooter: Hides the timeline footer and Tweet box, if included.'
            u''
            u'noborders: Removes all borders within the widget (between '
            u'Tweets, cards, around the widget.) See also: border-color.'
            u''
            u'noscrollbar: Crops and hides the main timeline scrollbar, if '
            u'visible. Please consider that hiding standard user interface '
            u'components can affect the accessibility of your website.'
            u''
            u'transparent: Removes the background color.'),
        values=("noheader", "nofooter", "noborders", "noscrollbar", 
                "transparent"),
        required=False,
        default="")

    border_color = schema.TextLine(
        title=_(u"Border color"),
        description=_(u'Change the border color used by the widget. Takes an '
            u'#abc123 hex format color e.g. "#cc0000"'),
        required=True)

    lang = schema.TextLine(
        title=_(u"Language"),
        description=_(u'The widget language is detected from the page, based '
            u'on the HTML lang attribute of your content. You can also set '
            u'the HTML lang attribute on the embed code itself.'),
        required=True)

    tweet_limit = schema.Int(
        title=_(u"Tweet limit"),
        description=_(u'To fix the size of a timeline to a preset number of '
            u'Tweets, use the data-tweet-limit="5" attribute with any value '
            u'between 1 and 20 Tweets. The timeline will render the specified '
            u'number of Tweets from the timeline, expanding the height of the '
            u'widget to display all Tweets without scrolling. Since the '
            u'widget is of a fixed size, it will not poll for updates when '
            u'using this option.'),
        required=False)

    related = schema.TextLine(
        title=_(u"Web Intent Related Users"),
        description=_(u'As per the Tweet and follow buttons, you may '
            u'provide a comma-separated list of user screen names as '
            u'suggested followers to a user after they reply, Retweet, or '
            u'favorite a Tweet in the timeline. Use a '
            u'data-related="benward,endform" attribute on the embed code.'),
        required=False)

    aria_polite = schema.Bool(
        title=_(u"ARIA politeness"),
        description=_(u'ARIA is an accessibility system that aids people '
            u'using assistive technology interacting with dynamic web '
            u"content. Read more about ARIA on W3C's website. If enabled, the "
            u'embedded timeline uses the least obtrusive setting. If using an '
            u'embedded timeline as a primary source of content on your page, '
            u'you may wish to override this to the assertive setting.'),
        # values=("polite", "assertive"),
        required=False,
        default=True)

    emulate_portlet = schema.Bool(
        title=_(u"Emulate portlet"),
        description=_(u'If enabled, the widget is set as unobtrusive as '
            u'possible and rendered in a portlet instead of the standard '
            u'Twitter widget.'),
        # values=("polite", "assertive"),
        required=False,
        default=False)



class Assignment(base.Assignment):
    """ Portlet assignment """
    implements(ITwitterWidgetPortlet)

    header = u""
    info = u""
    username = u""
    widget_id = u""
    theme = u""
    link_color = u""
    width = u""
    height = u""
    chrome = u""
    border_color = u""
    lang = u""
    tweet_limit = u""
    related = u""
    aria_polite = True
    emulate_portlet = False

    def __init__(self, header = u"", info = u"", username = u"", 
        widget_id = u"", theme = u"", link_color = u"", width = u"", 
        height = u"", chrome = u"", border_color = u"", lang = u"", 
        tweet_limit = u"", related = u"", aria_polite = True, 
        emulate_portlet = False):

        self.header = header
        self.info = info
        self.username = username
        self.widget_id = widget_id
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
    
    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Twitter Portlet: %s" % self.header


class Renderer(base.Renderer):
    """ Portlet renderer """

    render = ViewPageTemplateFile('twitterwidgetportlet.pt')


    def transformed(self, mt='text/x-html-safe'):
        """Use the safe_html transform to protect text output. This also
        ensures that resolve UID links are transformed into real links.
        """
        orig = self.data.info
        context = aq_inner(self.context)
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
            return unicode(result, 'utf-8')
        return None


class AddForm(base.AddForm):
    """ Portlet add form """
    form_fields = form.Fields(ITwitterWidgetPortlet)

    form_fields['info'].custom_widget = WYSIWYGWidget

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """ Portlet edit form """
    form_fields = form.Fields(ITwitterWidgetPortlet)

    form_fields['info'].custom_widget = WYSIWYGWidget
