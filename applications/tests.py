from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import JobSeekerProfile, RecruiterProfile
from companies.models import Company
from jobs.models import Job
from .models import Application

User = get_user_model()

class ApplicationAPITests(APITestCase):
    def setUp(self):
        # Job Seeker A
        self.seeker_a_user = User.objects.create_user(email="seekera@example.com",password="Password123!",role=User.Role.JOB_SEEKER,)
        self.seeker_a_profile = JobSeekerProfile.objects.create(user=self.seeker_a_user,phone="1111111111",location="Delhi",)

        # Job Seeker B
        self.seeker_b_user = User.objects.create_user(email="seekerb@example.com",password="Password123!",role=User.Role.JOB_SEEKER,)
        self.seeker_b_profile = JobSeekerProfile.objects.create(user=self.seeker_b_user,phone="2222222222", location="Mumbai",)

        # Recruiter A
        self.recruiter_a_user = User.objects.create_user(email="recruitera@example.com",password="Password123!",role=User.Role.RECRUITER,)
        self.recruiter_a_profile = RecruiterProfile.objects.create(user=self.recruiter_a_user,phone="3333333333",designation="Tech Lead",)

        # Recruiter B
        self.recruiter_b_user = User.objects.create_user(email="recruiterb@example.com",password="Password123!",role=User.Role.RECRUITER,)
        self.recruiter_b_profile = RecruiterProfile.objects.create(user=self.recruiter_b_user,phone="4444444444",designation="HR Manager",)

        # Companies
        self.company_a = Company.objects.create(recruiter=self.recruiter_a_profile,name="Company Alpha",location="Bangalore",)

        self.company_b = Company.objects.create(recruiter=self.recruiter_b_profile,name="Company Beta",location="Pune",)

        # Jobs
        self.active_job_1 = Job.objects.create(company=self.company_a, title="Backend Django Developer",description="Build scalable APIs.", salary_min=50000, salary_max=80000, is_active=True,)

        self.active_job_2 = Job.objects.create(company=self.company_b, title="Full Stack Engineer", description="React + Django", salary_min=60000, salary_max=90000, is_active=True,)

        self.inactive_job = Job.objects.create(company=self.company_a, title="Legacy PHP Developer", description="Closed position", is_active=False,)

        # Existing applications
        self.app_seeker_a = Application.objects.create(job_seeker=self.seeker_a_profile, job=self.active_job_1,cover_letter="Excited to join Company Alpha!",)

        self.app_seeker_b = Application.objects.create(
            job_seeker=self.seeker_b_profile,
            job=self.active_job_2,
            cover_letter="Looking forward to Company Beta!",
        )

        self.list_url = "/api/applications/"

    def detail_url(self, app_id):
        return f"/api/applications/{app_id}/"

    def get_results(self, response):
        data = response.data

        if isinstance(data, dict):
            return data.get("results", data)

        return data

    # ---------------- JOB SEEKER TESTS ----------------

    def test_job_seeker_apply_to_active_job(self):
        self.client.force_authenticate(user=self.seeker_a_user)

        payload = {
            "job": self.active_job_2.id,
            "cover_letter": "I am a great fit for this role.",
        }

        response = self.client.post(
            self.list_url, payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], Application.Status.APPLIED)

    def test_job_seeker_cannot_apply_to_same_job_twice(self):
        self.client.force_authenticate(user=self.seeker_a_user)

        payload = {
            "job": self.active_job_1.id,
            "cover_letter": "Applied again!",
        }

        response = self.client.post(
            self.list_url, payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_two_seekers_can_apply_to_same_job(self):
        self.client.force_authenticate(user=self.seeker_a_user)

        response = self.client.post(
            self.list_url,
            {"job": self.active_job_2.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_job_seeker_cannot_apply_to_inactive_job(self):
        self.client.force_authenticate(user=self.seeker_a_user)

        response = self.client.post(
            self.list_url,
            {"job": self.inactive_job.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_job_seeker_view_own_applications(self):
        self.client.force_authenticate(user=self.seeker_a_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = self.get_results(response)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.app_seeker_a.id)

    def test_job_seeker_cannot_view_other_seeker_application(self):
        self.client.force_authenticate(user=self.seeker_a_user)

        response = self.client.get(
            self.detail_url(self.app_seeker_b.id)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_job_seeker_cannot_update_application_status(self):
        self.client.force_authenticate(user=self.seeker_a_user)

        response = self.client.patch(
            self.detail_url(self.app_seeker_a.id),
            {"status": Application.Status.SELECTED},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_seeker_cannot_delete_application(self):
        self.client.force_authenticate(user=self.seeker_a_user)

        response = self.client.delete(
            self.detail_url(self.app_seeker_a.id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    # ---------------- RECRUITER TESTS ----------------

    def test_recruiter_a_views_own_applications(self):
        self.client.force_authenticate(user=self.recruiter_a_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = self.get_results(response)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.app_seeker_a.id)

    def test_recruiter_b_views_own_applications(self):
        self.client.force_authenticate(user=self.recruiter_b_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = self.get_results(response)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.app_seeker_b.id)

    def test_recruiter_cannot_view_another_recruiters_application(self):
        self.client.force_authenticate(user=self.recruiter_a_user)

        response = self.client.get(
            self.detail_url(self.app_seeker_b.id)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_recruiter_can_update_own_application_status(self):
        self.client.force_authenticate(user=self.recruiter_a_user)

        response = self.client.patch(
            self.detail_url(self.app_seeker_a.id),
            {"status": Application.Status.SHORTLISTED},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["status"],
            Application.Status.SHORTLISTED,
        )

        self.app_seeker_a.refresh_from_db()

        self.assertEqual(
            self.app_seeker_a.status,
            Application.Status.SHORTLISTED,
        )

    def test_recruiter_cannot_update_another_recruiters_application(self):
        self.client.force_authenticate(user=self.recruiter_a_user)

        response = self.client.patch(
            self.detail_url(self.app_seeker_b.id),
            {"status": Application.Status.REJECTED},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_recruiter_cannot_create_application(self):
        self.client.force_authenticate(user=self.recruiter_a_user)

        response = self.client.post(
            self.list_url,
            {"job": self.active_job_1.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_recruiter_cannot_delete_application(self):
        self.client.force_authenticate(user=self.recruiter_a_user)

        response = self.client.delete(
            self.detail_url(self.app_seeker_a.id)
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    # ---------------- STATUS BEHAVIOUR TESTS ----------------

    def test_updated_status_is_visible_to_job_seeker(self):
        self.client.force_authenticate(user=self.recruiter_a_user)

        patch_response = self.client.patch(
            self.detail_url(self.app_seeker_a.id),
            {"status": Application.Status.SHORTLISTED},
            format="json",
        )

        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.seeker_a_user)

        get_response = self.client.get(
            self.detail_url(self.app_seeker_a.id)
        )

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get_response.data["status"],
            Application.Status.SHORTLISTED,
        )

    def test_invalid_status_returns_400(self):
        self.client.force_authenticate(user=self.recruiter_a_user)

        response = self.client.patch(
            self.detail_url(self.app_seeker_a.id),
            {"status": "INVALID_STATUS"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)

    def test_job_seeker_cannot_submit_selected_status(self):
        self.client.force_authenticate(user=self.seeker_a_user)

        response = self.client.patch(
            self.detail_url(self.app_seeker_a.id),
            {"status": Application.Status.SELECTED},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.app_seeker_a.refresh_from_db()

        self.assertEqual(
            self.app_seeker_a.status,
            Application.Status.APPLIED,
        )

    # ---------------- AUTHENTICATION TESTS ----------------

    def test_unauthenticated_user_cannot_list_applications(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_unauthenticated_user_cannot_apply(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            self.list_url,
            {"job": self.active_job_1.id},
            format="json",
        )

        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )
