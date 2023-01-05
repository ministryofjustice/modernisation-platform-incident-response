from opgincidentresponse.actions.pagerduty import page_specialist
from opgincidentresponse.actions.keyword_handlers import status_page_notification, runbook_notification
from response.slack.models import CommsChannel

def test_status_page_notification(mocker):
    mocker.patch.object(CommsChannel, 'post_in_channel')
    
    status_page_notification(CommsChannel, '', '', '', '')

    CommsChannel.post_in_channel.assert_called_once_with("ℹ️ You mentioned the Status Page - You can find our statuspage here: https://theofficeofthepublicguardian.statuspage.io/")

def test_runbook_notification(mocker):
    mocker.patch.object(CommsChannel, 'post_in_channel')
    
    runbook_notification(CommsChannel, '', '', '', '')

    CommsChannel.post_in_channel.assert_called_once_with("ℹ️ You mentioned runbooks - You can find runbooks for our services here: https://ministryofjustice.github.io/opg-technical-guidance/#opg-technical-guidance/")