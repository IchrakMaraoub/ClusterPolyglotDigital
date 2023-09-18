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
 * @interface PatchedInvitation
 */
export interface PatchedInvitation {
    /**
     * 
     * @type {string}
     * @memberof PatchedInvitation
     */
    readonly id?: string;
    /**
     * 
     * @type {number}
     * @memberof PatchedInvitation
     */
    team?: number;
    /**
     * 
     * @type {string}
     * @memberof PatchedInvitation
     */
    email?: string;
    /**
     * 
     * @type {RoleEnum}
     * @memberof PatchedInvitation
     */
    role?: RoleEnum;
    /**
     * 
     * @type {string}
     * @memberof PatchedInvitation
     */
    readonly invitedBy?: string;
    /**
     * 
     * @type {boolean}
     * @memberof PatchedInvitation
     */
    isAccepted?: boolean;
}

/**
 * Check if a given object implements the PatchedInvitation interface.
 */
export function instanceOfPatchedInvitation(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function PatchedInvitationFromJSON(json: any): PatchedInvitation {
    return PatchedInvitationFromJSONTyped(json, false);
}

export function PatchedInvitationFromJSONTyped(json: any, ignoreDiscriminator: boolean): PatchedInvitation {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': !exists(json, 'id') ? undefined : json['id'],
        'team': !exists(json, 'team') ? undefined : json['team'],
        'email': !exists(json, 'email') ? undefined : json['email'],
        'role': !exists(json, 'role') ? undefined : RoleEnumFromJSON(json['role']),
        'invitedBy': !exists(json, 'invited_by') ? undefined : json['invited_by'],
        'isAccepted': !exists(json, 'is_accepted') ? undefined : json['is_accepted'],
    };
}

export function PatchedInvitationToJSON(value?: PatchedInvitation | null): any {
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

