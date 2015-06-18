# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Definition for conversion between legacy YAML and One Platform protos."""

from yaml_conversion import converters as c
from yaml_conversion import schema as s


SCHEMA = s.Message(
    api_config=s.Message(
        url=s.Value(converter=c.ToJsonString),
        login=s.Value(converter=c.EnumConverter('LOGIN')),
        secure=s.Value('security_level', converter=c.EnumConverter('SECURE')),
        auth_fail_action=s.Value(converter=c.EnumConverter('AUTH_FAIL_ACTION')),
        script=s.Value(converter=c.ToJsonString)),
    auto_id_policy=s.Value('beta_settings',
                           lambda val: {'auto_id_policy': val}),
    automatic_scaling=s.Message(
        cool_down_period_sec=s.Value('cool_down_period',
                                     converter=c.SecondsToDuration),
        cpu_utilization=s.Message(
            target_utilization=s.Value(),
            aggregation_window_length_sec=s.Value('aggregation_window_length',
                                                  converter=c.SecondsToDuration)
        ),
        max_num_instances=s.Value('max_total_instances'),
        min_pending_latency=s.Value(converter=c.LatencyToDuration),
        min_idle_instances=s.Value(converter=
                                   c.StringToInt(handle_automatic=True)),
        max_idle_instances=s.Value(converter=
                                   c.StringToInt(handle_automatic=True)),
        max_pending_latency=s.Value(converter=c.LatencyToDuration),
        max_concurrent_requests=s.Value(converter=c.StringToInt()),
        min_num_instances=s.Value('min_total_instances')),
    basic_scaling=s.Message(
        idle_timeout=s.Value(converter=c.IdleTimeoutToDuration),
        max_instances=s.Value(converter=c.StringToInt())),
    beta_settings=s.Map(),
    default_expiration=s.Value(converter=c.ExpirationToDuration),
    env_variables=s.Map(),
    error_handlers=s.RepeatedField(element=s.Message(
        error_code=s.Value(converter=c.EnumConverter('ERROR_CODE')),
        file=s.Value('static_file', converter=c.ToJsonString),
        mime_type=s.Value(converter=c.ToJsonString))),
    # Restructure the handler after it's complete, since this is more
    # complicated than a simple rename.
    handlers=s.RepeatedField(element=s.Message(
        converter=c.ConvertUrlHandler,
        auth_fail_action=s.Value(converter=c.EnumConverter('AUTH_FAIL_ACTION')),
        static_dir=s.Value(converter=c.ToJsonString),
        secure=s.Value('security_level', converter=c.EnumConverter('SECURE')),
        redirect_http_response_code=s.Value(
            converter=c.EnumConverter('REDIRECT_HTTP_RESPONSE_CODE')),
        http_headers=s.Map(),
        url=s.Value('url_regex'),
        expiration=s.Value(converter=c.ExpirationToDuration),
        static_files=s.Value('path', converter=c.ToJsonString),
        script=s.Value('script_path', converter=c.ToJsonString),
        upload=s.Value('upload_path_regex', converter=c.ToJsonString),
        api_endpoint=s.Value(),
        application_readable=s.Value(),
        position=s.Value(),
        login=s.Value(converter=c.EnumConverter('LOGIN')),
        mime_type=s.Value(converter=c.ToJsonString),
        require_matching_file=s.Value())),
    health_check=s.Message(
        check_interval_sec=s.Value('check_interval',
                                   converter=c.SecondsToDuration),
        timeout_sec=s.Value('timeout', converter=c.SecondsToDuration),
        healthy_threshold=s.Value(),
        enable_health_check=s.Value('disable_health_check', converter=c.Not),
        unhealthy_threshold=s.Value(),
        host=s.Value(converter=c.ToJsonString),
        restart_threshold=s.Value()),
    inbound_services=s.RepeatedField(element=s.Value(
        converter=c.EnumConverter('INBOUND_SERVICE'))),
    instance_class=s.Value(converter=c.ToJsonString),
    libraries=s.RepeatedField(element=s.Message(
        version=s.Value(converter=c.ToJsonString),
        name=s.Value(converter=c.ToJsonString))),
    manual_scaling=s.Message(
        instances=s.Value(converter=c.StringToInt())),
    network=s.Message(
        instance_tag=s.Value(converter=c.ToJsonString),
        name=s.Value(converter=c.ToJsonString),
        forwarded_ports=s.RepeatedField(element=s.Value(converter=
                                                        c.ToJsonString))),
    nobuild_files=s.Value('nobuild_files_regex', converter=c.ToJsonString),
    resources=s.Message(
        memory_gb=s.Value(),
        disk_size_gb=s.Value('disk_gb'),
        cpu=s.Value()),
    runtime=s.Value(converter=c.ToJsonString),
    threadsafe=s.Value(),
    vm=s.Value(),
    vm_settings=s.Map('beta_settings'))