/* tslint:disable */
/* eslint-disable */
/**
 * Qualifeed
 * Quality control application
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import type { RoleEnum } from './RoleEnum';
import {
    RoleEnumFromJSON,
    RoleEnumFromJSONTyped,
    RoleEnumToJSON,
} from './RoleEnum';

/**
 * 
 * @export
 * @interface Invitation
 */
export interface Invitation {
    /**
     * 
     * @type {string}
     * @memberof Invitation
     */
    readonly id: string;
    /**
     * 
     * @type {number}
     * @memberof Invitation
     */
    team: number;
    /**
     * 
     * @type {string}
     * @memberof Invitation
     */
    email: string;
    /**
     * 
     * @type {RoleEnum}
     * @memberof Invitation
     */
    role?: RoleEnum;
    /**
     * 
     * @type {string}
     * @memberof Invitation
     */
    readonly invitedBy: string;
    /**
     * 
     * @type {boolean}
     * @memberof Invitation
     */
    isAccepted?: boolean;
}

/**
 * Check if a given object implements the Invitation interface.
 */
export function instanceOfInvitation(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "team" in value;
    isInstance = isInstance && "email" in value;
    isInstance = isInstance && "invitedBy" in value;

    return isInstance;
}

export function InvitationFromJSON(json: any): Invitation {
    return InvitationFromJSONTyped(json, false);
}

export function InvitationFromJSONTyped(json: any, ignoreDiscriminator: boolean): Invitation {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'team': json['team'],
        'email': json['email'],
        'role': !exists(json, 'role') ? undefined : RoleEnumFromJSON(json['role']),
        'invitedBy': json['invited_by'],
        'isAccepted': !exists(json, 'is_accepted') ? undefined : json['is_accepted'],
    };
}

export function InvitationToJSON(value?: Invitation | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'team': value.team,
        'email': value.email,
        'role': RoleEnumToJSON(value.role),
        'is_accepted': value.isAccepted,
    };
}

