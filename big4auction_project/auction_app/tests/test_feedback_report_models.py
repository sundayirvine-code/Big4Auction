from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from auction_app.models import Feedback, Report, User, Item, Category

class FeedbackModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the Feedback model.
        """
        self.user = User.objects.create(username='feedback_user', phone_number='1234567890')
        self.feedback = Feedback.objects.create(
            user=self.user,
            rating=4,
            comment='This is a test feedback.',
            timestamp=timezone.now(),
        )

    def test_feedback_str(self):
        """
        Test the string representation of the Feedback model.
        """
        expected_str = f'Feedback #{self.feedback.pk} from {self.user.username}'
        self.assertEqual(str(self.feedback), expected_str)

    def test_feedback_validation(self):
        """
        Test validation of the Feedback model.
        """
        invalid_feedback = Feedback(
            user=None,  # User is required
            rating=2,  
            comment='',  # Comment should not be empty
            timestamp=None,  # Timestamp is required
        )
        with self.assertRaises(ValidationError) as context:
            invalid_feedback.full_clean()

        self.assertIn('This field cannot be null.', context.exception.error_dict['user'][0])
        self.assertIn('This field cannot be blank.', context.exception.error_dict['comment'][0])
        self.assertNotIn('timestamp', context.exception.error_dict)

    def test_feedback_rating_validation(self):
        """
        Test validation of the Feedback model's rating field.
        """
        # Valid rating
        feedback_valid = Feedback(
            user=self.user,
            rating=4,
            comment='This is a valid feedback.',
            timestamp=timezone.now(),
        )
        feedback_valid.full_clean()  # Should not raise any ValidationError

        # Invalid rating (less than 0)
        feedback_invalid_low = Feedback(
            user=self.user,
            rating=-1,
            comment='This rating is invalid.',
            timestamp=timezone.now(),
        )
        with self.assertRaises(ValidationError) as context:
            feedback_invalid_low.full_clean()
        self.assertIn('Ensure this value is greater than or equal to 0.', context.exception.error_dict['rating'][0])

        # Invalid rating (greater than 5)
        feedback_invalid_high = Feedback(
            user=self.user,
            rating=6,
            comment='This rating is also invalid.',
            timestamp=timezone.now(),
        )
        with self.assertRaises(ValidationError) as context:
            feedback_invalid_high.full_clean()
        self.assertIn('Ensure this value is less than or equal to 5.', context.exception.error_dict['rating'][0])

    def test_feedback_relationships(self):
        """
        Test relationships with User for the Feedback model.
        """
        self.assertEqual(self.feedback.user.username, 'feedback_user')

    def test_feedback_cascade_delete(self):
        """
        Test that deleting a user also deletes associated feedback.
        """
        user_id = self.feedback.user.id
        feedback_id = self.feedback.id

        self.feedback.user.delete()

        with self.assertRaises(Feedback.DoesNotExist):
            Feedback.objects.get(pk=feedback_id)

    def test_feedback_lifecycle(self):
        """
        Test the lifecycle of the Feedback model.
        """
        initial_comment = self.feedback.comment

        # Modify the feedback comment
        self.feedback.comment = 'Modified Comment'
        self.feedback.save()

        self.assertNotEqual(self.feedback.comment, initial_comment)

        # Delete the feedback
        feedback_id = self.feedback.id
        self.feedback.delete()

        with self.assertRaises(Feedback.DoesNotExist):
            Feedback.objects.get(pk=feedback_id)


class ReportModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the Report model.
        """
        self.reporter_user = User.objects.create(username='reporter_user', phone_number='1234567890')
        self.reported_user = User.objects.create(username='reported_user', phone_number='9876543210')
        category = Category.objects.create(category_name='Test Category')
        self.item = Item.objects.create(
            title='Test Item',
            slug='test-item',
            description='This is a test item.',
            category=category,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=7),
            created=timezone.now(),
            starting_bid=10.00,
            reserve_price=20.00,
            current_bid=15.00,
            status='active',
        )
        self.report = Report.objects.create(
            reporter=self.reporter_user,
            reported_user=self.reported_user,
            item=self.item,
            report_description='This is a test report.',
            timestamp=timezone.now(),
        )

    def test_report_str(self):
        """
        Test the string representation of the Report model.
        """
        expected_str = f'Report #{self.report.pk} by {self.reporter_user.username} against {self.reported_user.username}'
        self.assertEqual(str(self.report), expected_str)

    def test_report_validation(self):
        """
        Test validation of the Report model.
        """
        invalid_report = Report(
            reporter=None,  # Reporter is required
            reported_user=None,  # Reported user is required
            item=None,  # Item can be null or blank
            report_description='',  # Description should not be empty
            timestamp=None,  # Timestamp is required
        )
        with self.assertRaises(ValidationError) as context:
            invalid_report.full_clean()

        # Check exact error messages
        self.assertIn('This field cannot be null.', context.exception.error_dict['reporter'][0])
        self.assertIn('This field cannot be null.', context.exception.error_dict['reported_user'][0])
        self.assertIn('This field cannot be blank.', context.exception.error_dict['report_description'][0])
        # Check for the absence of timestamp field in the error_dict
        self.assertNotIn('timestamp', context.exception.error_dict)

    def test_report_relationships(self):
        """
        Test relationships with User and Item for the Report model.
        """
        self.assertEqual(self.report.reporter.username, 'reporter_user')
        self.assertEqual(self.report.reported_user.username, 'reported_user')
        self.assertEqual(self.report.item.title, 'Test Item')

    def test_report_cascade_delete(self):
        """
        Test that deleting a user or item also deletes associated reports.
        """
        reporter_user_id = self.report.reporter.id
        reported_user_id = self.report.reported_user.id
        item_id = self.report.item.id

        self.report.reporter.delete()
        self.report.reported_user.delete()
        self.report.item.delete()

        with self.assertRaises(Report.DoesNotExist):
            Report.objects.get(pk=self.report.pk)

    def test_report_lifecycle(self):
        """
        Test the lifecycle of the Report model.
        """
        initial_description = self.report.report_description

        # Modify the report description
        self.report.report_description = 'Modified Description'
        self.report.save()

        self.assertNotEqual(self.report.report_description, initial_description)

        # Delete the report
        report_id = self.report.id
        self.report.delete()

        with self.assertRaises(Report.DoesNotExist):
            Report.objects.get(pk=report_id)
