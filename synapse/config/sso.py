# -*- coding: utf-8 -*-
# Copyright 2020 The Matrix.org Foundation C.I.C.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Any, Dict

import pkg_resources

from ._base import Config, ConfigError


class SSOConfig(Config):
    """SSO Configuration
    """

    section = "sso"

    def read_config(self, config, **kwargs):
        sso_config = config.get("sso") or {}  # type: Dict[str, Any]

        # Pick a template directory in order of:
        # * The sso-specific template_dir
        # * /path/to/synapse/install/res/templates
        template_dir = sso_config.get("template_dir")
        if not template_dir:
            template_dir = pkg_resources.resource_filename("synapse", "res/templates",)

        self.sso_redirect_confirm_template_dir = template_dir

    def generate_config_section(self, **kwargs):
        return """\
        # Additional settings to use with single-sign on systems such as SAML2 and CAS.
        #
        sso:
            # Directory in which Synapse will try to find the template files below.
            # If not set, default templates from within the Synapse package will be used.
            #
            # DO NOT UNCOMMENT THIS SETTING unless you want to customise the templates.
            # If you *do* uncomment it, you will need to make sure that all the templates
            # below are in the directory.
            #
            # Synapse will look for the following templates in this directory:
            #
            # * HTML page for a confirmation step before redirecting back to the client
            #   with the login token: 'sso_redirect_confirm.html'.
            #
            #   When rendering, this template is given three variables:
            #     * redirect_url: the URL the user is about to be redirected to. Needs
            #                     manual escaping (see
            #                     https://jinja.palletsprojects.com/en/2.11.x/templates/#html-escaping).
            #
            #     * display_url: the same as `redirect_url`, but with the query
            #                    parameters stripped. The intention is to have a
            #                    human-readable URL to show to users, not to use it as
            #                    the final address to redirect to. Needs manual escaping
            #                    (see https://jinja.palletsprojects.com/en/2.11.x/templates/#html-escaping).
            #
            #     * server_name: the homeserver's name.
            #
            # You can see the default templates at:
            # https://github.com/matrix-org/synapse/tree/master/synapse/res/templates
            #
            #template_dir: "res/templates"
        """