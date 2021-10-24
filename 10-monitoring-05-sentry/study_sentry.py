#!/usr/bin/env python3

import sentry_sdk

sentry_sdk.init(
    "https://a9ff9583d80e45eea8f023ccaa295346@o1050545.ingest.sentry.io/6031815",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

def factorial(x):
    if x == 1:
        return 1
    else:
        return (x * factorial(x-1))


num = 3000000
print("The factorial of", num, "is", factorial(num))