@e2e
Feature: KSeF Web API
    Log in, generate token, send invoice and list existing invoices

    Scenario: End to end
        Given signed in using cert
        When generate token
        Then sign in using token
        Then send an invoice
